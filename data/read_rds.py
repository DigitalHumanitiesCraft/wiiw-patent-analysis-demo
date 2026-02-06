"""
Minimal RDS reader for R serialization format v2/v3.
Reads common R types: data.frame, vectors (character, integer, real, logical).
"""

import gzip
import struct
import io
import pandas as pd
import sys

# R SEXP type constants
sys.setrecursionlimit(10000)
NILSXP = 0
SYMSXP = 1
LISTSXP = 2
CLOSXP = 3
ENVSXP = 4
PROMSXP = 5
LANGSXP = 6
SPECIALSXP = 7
BUILTINSXP = 8
CHARSXP = 9
LGLSXP = 10
INTSXP = 13
REALSXP = 14
CPLXSXP = 15
STRSXP = 16
DOTSXP = 17
ANYSXP = 18
VECSXP = 19
EXPRSXP = 20
BCODESXP = 21
EXTPTRSXP = 22
WEAKREFSXP = 23
RAWSXP = 24
S4SXP = 25
NEWSXP = 30
FREESXP = 31
REFSXP = 255
NAMESPACESXP = 249
PACKAGESSXP = 250
PERSISTSXP = 251
CLASSINFOSXP = 252
BCREPDEF = 244
BCREPREF = 243
EMPTYENV_SXP = 242
BASEENV_SXP = 241
GLOBALENV_SXP = 240
NILVALUE_SXP = 254
MISSINGARG_SXP = 251
BASENAMESPACE_SXP = 246
ATTRLANGSXP = 241
ATTRLISTSXP = 239

# Flags
HAS_ATTR = 1 << 9
HAS_TAG = 1 << 10
IS_OBJECT = 1 << 8


class RDSReader:
    def __init__(self, data):
        self.data = data
        self.pos = 0
        self.ref_table = [None]  # 1-indexed

    def read_bytes(self, n):
        result = self.data[self.pos:self.pos + n]
        self.pos += n
        return result

    def read_int(self):
        result = struct.unpack('>i', self.read_bytes(4))[0]
        return result

    def read_double(self):
        result = struct.unpack('>d', self.read_bytes(8))[0]
        return result

    def read_string(self, length):
        return self.read_bytes(length)

    def read_header(self):
        # Read format identifier
        fmt = chr(self.data[0])
        assert self.data[1] == ord('\n')
        self.pos = 2

        version = self.read_int()
        writer_version = self.read_int()
        min_reader_version = self.read_int()

        info = {
            'format': fmt,
            'version': version,
            'writer_version': writer_version,
            'min_reader_version': min_reader_version,
        }

        if version >= 3:
            enc_len = self.read_int()
            encoding = self.read_string(enc_len).decode('ascii')
            info['encoding'] = encoding

        return info

    def read_flags(self):
        flags = self.read_int()
        stype = flags & 0xFF
        levels = flags >> 12
        has_attr = bool(flags & HAS_ATTR)
        has_tag = bool(flags & HAS_TAG)
        is_object = bool(flags & IS_OBJECT)
        return stype, levels, has_attr, has_tag, is_object

    def read_item(self):
        flags = self.read_int()
        stype = flags & 0xFF
        levels = flags >> 12
        has_attr = bool(flags & HAS_ATTR)
        has_tag = bool(flags & HAS_TAG)
        is_object = bool(flags & IS_OBJECT)

        return self._read_item_inner(stype, levels, has_attr, has_tag, is_object)

    def _read_item_inner(self, stype, levels, has_attr, has_tag, is_object):
        result = None

        if stype == NILVALUE_SXP:
            return None

        elif stype == NILSXP:
            return None

        elif stype == REFSXP:
            ref_idx = levels  # packed reference index
            if ref_idx == 0:
                ref_idx = self.read_int()
            return self.ref_table[ref_idx]

        elif stype == SYMSXP:
            name_item = self.read_item()
            if isinstance(name_item, bytes):
                name_item = name_item.decode('utf-8', errors='replace')
            self.ref_table.append(name_item)
            return name_item

        elif stype == CHARSXP:
            length = self.read_int()
            if length == -1:
                return None  # NA_STRING
            s = self.read_string(length)
            try:
                return s.decode('utf-8')
            except:
                return s.decode('latin-1', errors='replace')

        elif stype == STRSXP:
            length = self.read_int()
            result = []
            for _ in range(length):
                result.append(self.read_item())
            if has_attr:
                self.read_item()  # read and discard attributes
            return result

        elif stype == INTSXP:
            length = self.read_int()
            result = []
            for _ in range(length):
                val = self.read_int()
                result.append(None if val == -2147483648 else val)  # NA_INTEGER
            if has_attr:
                attrs = self.read_item()
                # Check if this is a factor
                if isinstance(attrs, dict) and 'class' in attrs and 'factor' in str(attrs.get('class', '')):
                    levels = attrs.get('levels', [])
                    result = [levels[v - 1] if v is not None and 1 <= v <= len(levels) else None for v in result]
            return result

        elif stype == REALSXP:
            length = self.read_int()
            result = []
            for _ in range(length):
                result.append(self.read_double())
            if has_attr:
                self.read_item()
            return result

        elif stype == LGLSXP:
            length = self.read_int()
            result = []
            for _ in range(length):
                val = self.read_int()
                result.append(None if val == -2147483648 else bool(val))
            if has_attr:
                self.read_item()
            return result

        elif stype == VECSXP:
            length = self.read_int()
            items = []
            for _ in range(length):
                items.append(self.read_item())

            attrs = None
            if has_attr:
                attrs = self.read_item()

            if is_object and isinstance(attrs, dict):
                # data.frame
                names = attrs.get('names', [])
                if names and len(names) == len(items):
                    return {n: v for n, v in zip(names, items)}

            return items

        elif stype == LISTSXP:
            # Pairlist - used for attributes
            result = {}
            tag = None
            if has_attr:
                self.read_item()  # discard pairlist attributes
            if has_tag:
                tag = self.read_item()
            car = self.read_item()
            cdr = self.read_item()

            if tag is not None:
                result[tag] = car
            if isinstance(cdr, dict):
                result.update(cdr)
            return result

        elif stype == RAWSXP:
            length = self.read_int()
            result = self.read_bytes(length)
            if has_attr:
                self.read_item()
            return result

        elif stype in (GLOBALENV_SXP, 240):
            return '<globalenv>'

        elif stype in (BASEENV_SXP, 241):
            return '<baseenv>'

        elif stype in (EMPTYENV_SXP, 242):
            return '<emptyenv>'

        elif stype == NAMESPACESXP:
            self.read_item()
            return '<namespace>'

        elif stype == LANGSXP or stype == 6:
            if has_attr:
                self.read_item()
            if has_tag:
                self.read_item()
            self.read_item()  # car
            self.read_item()  # cdr
            return '<lang>'

        elif stype == EXTPTRSXP or stype == 22:
            # External pointer: protected, tag, then ref
            self.read_item()  # protected
            self.read_item()  # tag
            return '<externalptr>'

        elif stype == CLOSXP or stype == 3:
            if has_attr:
                self.read_item()
            self.read_item()  # env
            self.read_item()  # formals
            self.read_item()  # body
            return '<closure>'

        elif stype == ENVSXP or stype == 4:
            self.ref_table.append('<env>')
            locked = self.read_int()
            self.read_item()  # enclos
            self.read_item()  # frame
            self.read_item()  # hashtab
            self.read_item()  # attributes
            return '<env>'

        elif stype == S4SXP or stype == 25:
            if has_attr:
                self.read_item()
            if has_tag:
                self.read_item()
            return '<S4>'

        else:
            raise ValueError(f"Unsupported SEXP type: {stype} at position {self.pos}")


def read_rds(filepath):
    with open(filepath, 'rb') as f:
        raw = f.read()

    if raw[:2] == b'\x1f\x8b':
        raw = gzip.decompress(raw)

    reader = RDSReader(raw)
    header = reader.read_header()
    print(f"RDS format: {header['format']}, version: {header['version']}")
    if 'encoding' in header:
        print(f"Encoding: {header['encoding']}")

    obj = reader.read_item()
    return obj


def main():
    filepath = 'db_networkCoPat_fake.rds'

    print("=" * 70)
    print("READING RDS FILE")
    print("=" * 70)

    obj = read_rds(filepath)

    if isinstance(obj, dict):
        print(f"\nObject type: data.frame (dict with {len(obj)} columns)")

        df = pd.DataFrame(obj)

        print(f"\n{'=' * 70}")
        print("STRUCTURE")
        print(f"{'=' * 70}")
        print(f"Rows: {len(df):,}")
        print(f"Columns: {len(df.columns)}")
        print(f"\nColumn names and types:")
        for col in df.columns:
            non_null = df[col].notna().sum()
            null_count = df[col].isna().sum()
            dtype = df[col].dtype
            print(f"  {col:<30} {str(dtype):<15} non-null: {non_null:>8,}  NA: {null_count:>6,}")

        print(f"\n{'=' * 70}")
        print("BASIC STATISTICS")
        print(f"{'=' * 70}")

        # Numeric columns
        numeric_cols = df.select_dtypes(include=['number']).columns
        if len(numeric_cols) > 0:
            print("\nNumeric columns:")
            print(df[numeric_cols].describe().to_string())

        # Non-numeric columns
        obj_cols = df.select_dtypes(include=['object']).columns
        if len(obj_cols) > 0:
            print("\nCategorical / String columns:")
            for col in obj_cols:
                n_unique = df[col].nunique()
                top_vals = df[col].value_counts().head(5)
                print(f"\n  {col} ({n_unique:,} unique values)")
                print(f"    Top 5:")
                for val, count in top_vals.items():
                    print(f"      {val}: {count:,}")

        print(f"\n{'=' * 70}")
        print("SAMPLE (50 rows)")
        print(f"{'=' * 70}")
        sample = df.sample(n=min(50, len(df)), random_state=42)
        pd.set_option('display.max_columns', None)
        pd.set_option('display.width', 200)
        pd.set_option('display.max_colwidth', 40)
        print(sample.to_string())

    else:
        print(f"Object type: {type(obj)}")
        print(repr(obj)[:2000])


if __name__ == '__main__':
    main()
