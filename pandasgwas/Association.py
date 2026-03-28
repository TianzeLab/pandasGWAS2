from copy import deepcopy
from pandas import DataFrame, set_option

set_option('display.max_columns', None)
set_option('display.width', 1000)
set_option('display.colheader_justify', 'center')
set_option('display.precision', 3)


class Association:
    ASSOCIATION_COLUMNS = [
        'association_id',
        'risk_frequency',
        'pvalue_description',
        'pvalue_mantissa',
        'pvalue_exponent',
        'multi_snp_haplotype',
        'snp_interaction',
        'snp_type',
        'range',
        'description',
        'or_per_copy_num',
        'or_value',
        'beta_num',
        'beta_unit',
        'beta_direction',
        'beta',
        'last_mapping_date',
        'last_update_date',
        'p_value',
        'pubmed_id',
        'first_author',
        'ci_lower',
        'ci_upper'
    ]

    EFO_TRAITS_COLUMNS = ['association_id', 'efo_id', 'efo_trait']
    SNP_ALLELE_COLUMNS = ['association_id', 'rs_id', 'effect_allele']
    BG_EFO_TRAITS_COLUMNS = ['association_id', 'efo_id', 'efo_trait']
    REPORTED_TRAITS_COLUMNS = ['association_id', 'reported_trait']
    LOCATIONS_COLUMNS = ['association_id', 'location']
    MAPPED_GENES_COLUMNS = ['association_id', 'mapped_gene']
    SNP_EFFECT_ALLELES_COLUMNS = ['association_id', 'snp_effect_allele']

    # 真实字段名 -> 示例字段名
    FIELD_ALIASES = {
        'reported_traits': 'reported_trait',
        'snp_effect_alleles': 'snp_effect_allele'
    }

    NESTED_FIELDS = [
        'efo_traits',
        'snp_allele',
        'bg_efo_traits',
        'reported_trait',
        'locations',
        'mapped_genes',
        'snp_effect_allele'
    ]

    def __init__(self, data: list = None, mode: str = "Fat"):
        if mode not in ['Thin', 'Fat']:
            raise Exception("Mode must be Fat or Thin")
        if data is None:
            data = []
        else:
            data = [
                self._coerce_association_id(item)
                for item in data
                if isinstance(item, dict)
            ]


        self.mode = mode

        # Thin 模式：仅去掉 links/_links，其它不动
        if mode == "Thin":
            self.raw_data = [self._remove_links_only(item) for item in data if isinstance(item, dict)]
            return

        # Fat 模式：先标准化字段名、去掉 links/_links、补齐缺失字段
        standardized_data = []
        for item in data:
            if isinstance(item, dict):
                standardized_data.append(self._standardize_record(item))

        self.raw_data = standardized_data

        if len(standardized_data) == 0:
            self._init_empty_tables()
            return

        association_rows = []
        efo_traits_rows = []
        snp_allele_rows = []
        bg_efo_traits_rows = []
        reported_traits_rows = []
        locations_rows = []
        mapped_genes_rows = []
        snp_effect_alleles_rows = []

        for record in standardized_data:
            association_id = record.get('association_id', None)

            # 主表：固定字段，缺失补 None
            association_rows.append({
                col: record.get(col, None) for col in self.ASSOCIATION_COLUMNS
            })

            # efo_traits
            for item in self._ensure_list(record.get('efo_traits', None)):
                if isinstance(item, dict):
                    efo_traits_rows.append({
                        'association_id': association_id,
                        'efo_id': item.get('efo_id', None),
                        'efo_trait': item.get('efo_trait', None)
                    })
                else:
                    efo_traits_rows.append({
                        'association_id': association_id,
                        'efo_id': None,
                        'efo_trait': item
                    })

            # snp_allele
            for item in self._ensure_list(record.get('snp_allele', None)):
                if isinstance(item, dict):
                    snp_allele_rows.append({
                        'association_id': association_id,
                        'rs_id': item.get('rs_id', None),
                        'effect_allele': item.get('effect_allele', None)
                    })
                else:
                    snp_allele_rows.append({
                        'association_id': association_id,
                        'rs_id': item,
                        'effect_allele': None
                    })

            # bg_efo_traits
            for item in self._ensure_list(record.get('bg_efo_traits', None)):
                if isinstance(item, dict):
                    bg_efo_traits_rows.append({
                        'association_id': association_id,
                        'efo_id': item.get('efo_id', None),
                        'efo_trait': item.get('efo_trait', None)
                    })
                else:
                    bg_efo_traits_rows.append({
                        'association_id': association_id,
                        'efo_id': None,
                        'efo_trait': item
                    })

            # reported_traits（属性名保持不变，数据字段统一用 reported_trait）
            for item in self._ensure_list(record.get('reported_trait', None)):
                reported_traits_rows.append({
                    'association_id': association_id,
                    'reported_trait': item
                })

            # locations
            for item in self._ensure_list(record.get('locations', None)):
                locations_rows.append({
                    'association_id': association_id,
                    'location': item
                })

            # mapped_genes
            for item in self._ensure_list(record.get('mapped_genes', None)):
                mapped_genes_rows.append({
                    'association_id': association_id,
                    'mapped_gene': item
                })

            # snp_effect_alleles（属性名保持不变，数据字段统一用 snp_effect_allele）
            for item in self._ensure_list(record.get('snp_effect_allele', None)):
                snp_effect_alleles_rows.append({
                    'association_id': association_id,
                    'snp_effect_allele': item
                })

        self.associations = self._build_df(association_rows, self.ASSOCIATION_COLUMNS)
        self.efo_traits = self._build_df(efo_traits_rows, self.EFO_TRAITS_COLUMNS)
        self.snp_allele = self._build_df(snp_allele_rows, self.SNP_ALLELE_COLUMNS)
        self.bg_efo_traits = self._build_df(bg_efo_traits_rows, self.BG_EFO_TRAITS_COLUMNS)
        self.reported_traits = self._build_df(reported_traits_rows, self.REPORTED_TRAITS_COLUMNS)
        self.locations = self._build_df(locations_rows, self.LOCATIONS_COLUMNS)
        self.mapped_genes = self._build_df(mapped_genes_rows, self.MAPPED_GENES_COLUMNS)
        self.snp_effect_alleles = self._build_df(snp_effect_alleles_rows, self.SNP_EFFECT_ALLELES_COLUMNS)

    def _init_empty_tables(self):
        self.associations = DataFrame(columns=self.ASSOCIATION_COLUMNS)
        self.efo_traits = DataFrame(columns=self.EFO_TRAITS_COLUMNS)
        self.snp_allele = DataFrame(columns=self.SNP_ALLELE_COLUMNS)
        self.bg_efo_traits = DataFrame(columns=self.BG_EFO_TRAITS_COLUMNS)
        self.reported_traits = DataFrame(columns=self.REPORTED_TRAITS_COLUMNS)
        self.locations = DataFrame(columns=self.LOCATIONS_COLUMNS)
        self.mapped_genes = DataFrame(columns=self.MAPPED_GENES_COLUMNS)
        self.snp_effect_alleles = DataFrame(columns=self.SNP_EFFECT_ALLELES_COLUMNS)

    @staticmethod
    def _build_df(rows, columns):
        if len(rows) == 0:
            return DataFrame(columns=columns)
        return DataFrame(rows).reindex(columns=columns)

    @staticmethod
    def _ensure_list(value):
        if value is None:
            return []
        if isinstance(value, list):
            return value
        return [value]

    @staticmethod
    def _coerce_association_id(record: dict) -> dict:
        rec = deepcopy(record)
        if 'association_id' in rec and rec['association_id'] is not None:
            rec['association_id'] = str(rec['association_id'])
        return rec
    @staticmethod
    def _remove_links_only(record: dict) -> dict:
        rec = deepcopy(record)
        rec.pop('links', None)
        rec.pop('_links', None)
        return rec

    def _standardize_record(self, record: dict) -> dict:
        record = self._remove_links_only(record)

        # 第一步：字段别名统一成示例字段名
        normalized = {}
        for key, value in record.items():
            std_key = self.FIELD_ALIASES.get(key, key)
            normalized[std_key] = value

        # 第二步：主表字段全部补齐，缺失为 None
        standardized = {}
        for col in self.ASSOCIATION_COLUMNS:
            value = normalized.get(col, None)

            # range 最终统一保留字符串
            if col == 'range':
                value = self._normalize_range(value)

            standardized[col] = value

        # 第三步：嵌套字段统一补齐
        for field in self.NESTED_FIELDS:
            standardized[field] = normalized.get(field, None)

        return standardized

    @staticmethod
    def _normalize_range(value):
        if value is None:
            return None
        if isinstance(value, list):
            if len(value) == 0:
                return None
            if len(value) == 1:
                return None if value[0] is None else str(value[0])
            return '; '.join('' if v is None else str(v) for v in value)
        return str(value)

    def __str__(self):
        if self.mode == 'Fat':
            return (
                    "Association is running in fat mode. It has 8 DataFrames with hierarchical dependencies.\n"
                    "associations: %d rows\n"
                    "|\n -efo_traits: %d rows\n"
                    "|\n -snp_allele: %d rows\n"
                    "|\n -bg_efo_traits: %d rows\n"
                    "|\n -reported_traits: %d rows\n"
                    "|\n -locations: %d rows\n"
                    "|\n -mapped_genes: %d rows\n"
                    "|\n -snp_effect_alleles: %d rows"
                    % (
                        len(self.associations),
                        len(self.efo_traits),
                        len(self.snp_allele),
                        len(self.bg_efo_traits),
                        len(self.reported_traits),
                        len(self.locations),
                        len(self.mapped_genes),
                        len(self.snp_effect_alleles),
                    )
            )
        if self.mode == 'Thin':
            return (
                    'Association is running in thin mode. It has 1 list that contains the raw data.\n'
                    'raw_data: a list of size %d.'
                    % len(self.raw_data)
            )

    def __repr__(self):
        return self.__str__()

    def __getitem__(self, item):
        if isinstance(item, (str, int)):
            arr = [item]
        elif isinstance(item, (list, tuple, range)):
            arr = item
        elif isinstance(item, slice):
            start, stop, step = item.indices(len(self))
            arr = list(range(start, stop, step))
        else:
            raise TypeError('Invalid argument type: {}'.format(type(item)))

        raw_data = self.raw_data
        raw_data_dict = {}
        for j in raw_data:
            raw_data_dict[j['association_id']] = j

        sub_set = []
        for i in arr:
            if isinstance(i, str):
                sub_set.append(raw_data_dict[i])
            elif isinstance(i, int):
                sub_set.append(raw_data[i])
            else:
                raise TypeError('Invalid item type: {}'.format(type(i)))

        return Association(sub_set, self.mode)

    def __add__(self, other):
        if self.mode == other.mode:
            return Association(self.raw_data + other.raw_data, self.mode)
        else:
            raise Exception("Please input the same mode")

    def __sub__(self, other):
        if self.mode == other.mode:
            self_key_set = set()
            self_dict = {}
            other_key_set = set()

            for i in self.raw_data:
                self_key_set.add(i['association_id'])
                self_dict[i['association_id']] = i

            for j in other.raw_data:
                other_key_set.add(j['association_id'])

            sub_key = self_key_set - other_key_set
            data = []
            for k in sub_key:
                data.append(self_dict[k])

            return Association(data, self.mode)
        else:
            raise Exception("Please input the same mode")

    def __and__(self, other):
        if self.mode == other.mode:
            self_key_set = set()
            self_dict = {}
            other_key_set = set()

            for i in self.raw_data:
                self_key_set.add(i['association_id'])
                self_dict[i['association_id']] = i

            for j in other.raw_data:
                other_key_set.add(j['association_id'])

            sub_key = self_key_set & other_key_set
            data = []
            for k in sub_key:
                data.append(self_dict[k])

            return Association(data, self.mode)
        else:
            raise Exception("Please input the same mode")

    def __or__(self, other):
        if self.mode == other.mode:
            and_dict = {}

            for i in self.raw_data:
                and_dict[i['association_id']] = i

            for j in other.raw_data:
                and_dict[j['association_id']] = j

            data = list(and_dict.values())
            return Association(data, self.mode)
        else:
            raise Exception("Please input the same mode")

    def __xor__(self, other):
        if self.mode == other.mode:
            self_key_set = set()
            and_dict = {}
            other_key_set = set()

            for i in self.raw_data:
                self_key_set.add(i['association_id'])
                and_dict[i['association_id']] = i

            for j in other.raw_data:
                other_key_set.add(j['association_id'])
                and_dict[j['association_id']] = j

            sub_key = self_key_set ^ other_key_set
            data = []
            for k in sub_key:
                data.append(and_dict[k])

            return Association(data, self.mode)
        else:
            raise Exception("Please input the same mode")

    def __eq__(self, other):
        if self is None or other is None:
            return self is None and other is None
        return self.raw_data == other.raw_data and self.mode == other.mode

    def __len__(self):
        return len(self.raw_data)



