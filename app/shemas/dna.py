from pydantic import BaseModel, validator
import re


class Dna(BaseModel):
    dna: str

    @validator('dna')
    def check(cls, v):

        gen = '''tgacccactaatcagcaacatagcactttgagcaaaggcctgtgttggagctattggccc
caaaactgcctttccctaaacagtgttcaccattgtagacctcaccactgttcgcgtaac
aactggcatgtcctgggggttaatactcac'''

        nucleotide = ('a', 'c', 't', 'g')

        if re.search('(' + nucleotide[0] + '|' + nucleotide[1] + '|' + nucleotide[2] + '|' + nucleotide[3] + '){3}', v) is None:
            raise ValueError('Доступны только символы: a,c,t,g')
        if re.search(v, gen) is None:
            raise ValueError('Вхождение не найдено')
        if len(v) != 3:
            raise ValueError('Длина строки должна быть 3 символа')

        return v
