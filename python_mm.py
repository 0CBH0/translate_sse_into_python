import os, sys, re

show = lambda x: [hex(i) for i in x]
HIDWORD = lambda x: (x >> 32) & 0xFFFFFFFF

str2byte = lambda x: [int(x[i:(i+2)], 16) for i in range(0, len(x), 2)]
xmm2int = lambda x: [(x[y+3] << 24) | (x[y+2] << 16) | (x[y+1] << 8) | x[y] for y in range(0, 16, 4)]
int2xmm = lambda x: str2byte("".join(["".join([hex(x[y])[2:].zfill(8)[z:(z+2)] for z in range(0, 8, 2)][::-1]) for y in range(4)]))
xmm2long = lambda x: [(x[y+7] << 56) | (x[y+6] << 48) | (x[y+5] << 40) | (x[y+4] << 32) | (x[y+3] << 24) | (x[y+2] << 16) | (x[y+1] << 8) | x[y] for y in range(0, 16, 8)]
long2xmm = lambda x: str2byte("".join(["".join([hex(x[y])[2:].zfill(16)[z:(z+2)] for z in range(0, 16, 2)][::-1]) for y in range(2)]))
_mm_cvtsi32_si128 = lambda x: [int(hex(x)[2:].zfill(32)[i:(i+2)], 16) for i in range(0, 32, 2)][::-1]
_mm_extract_epi16 = lambda a, b: (a[b * 2 + 1] << 8) | a[b * 2]

def _mm_add_epi32(a, b):
    ai = xmm2int(a)
    bi = xmm2int(b)
    return int2xmm([(ai[x] + bi[x]) & 0xFFFFFFFF for x in range(len(ai))])

def _mm_mul_epu32(a, b):
    ai = xmm2int(a)
    bi = xmm2int(b)
    return long2xmm([(ai[x] * bi[x]) & 0xFFFFFFFFFFFFFFFF for x in [0, 2]])

def _mm_sub_epi32(a, b):
    ai = xmm2int(a)
    bi = xmm2int(b)
    for x in range(len(ai)):
        if ai[x] >= bi[x]:
            ai[x] -= bi[x]
        else:
            ai[x] = 0x100000000 + ai[x] - bi[x]
    return int2xmm(ai)

def _mm_or_si128(a, b):
    return [a[x] | b[x] for x in range(len(a))]

def _mm_shuffle_epi32(a, b):
    ai = xmm2int(a)
    if b == 0:
        return int2xmm([ai[0], ai[0], ai[0], ai[0]])
    if b == 8:
        return int2xmm([ai[0], ai[2], ai[0], ai[0]])
    print("???")
    return a

def _mm_shuffle_epi8(a, b):
    c = []
    for x in range(len(a)):
        if b[x] >= 0x80:
            c.append(0)
        else:
            c.append(a[b[x] % 16])
    return c

def _mm_slli_epi32(a, b):
    ai = xmm2int(a)
    return int2xmm([(ai[x] << b) & 0xFFFFFFFF for x in range(len(ai))])

def _mm_srli_epi32(a, b):
    ai = xmm2int(a)
    return int2xmm([(ai[x] >> b) & 0xFFFFFFFF for x in range(len(ai))])

def _mm_srli_epi64(a, b):
    ai = xmm2long(a)
    return long2xmm([(ai[x] >> b) & 0xFFFFFFFFFFFFFFFF for x in range(len(ai))])

def _mm_unpacklo_epi32(a, b):
    ai = xmm2int(a)
    bi = xmm2int(b)
    return int2xmm([ai[0], bi[0], ai[1], bi[1]])


# srdnlen\knight_s.enigma
_mm_add_epi64
_mm_add_epi8
_mm_and_si128
_mm_andnot_si128
_mm_cmpeq_epi16
_mm_cmpgt_epi32
_mm_cvtsi128_si32
_mm_insert_epi16
_mm_load_si128
_mm_loadu_si128
_mm_packus_epi16
_mm_shuffle_ps
_mm_shufflelo_epi16
_mm_slli_epi16
_mm_slli_epi64
_mm_srai_epi32
_mm_srli_epi16
_mm_unpackhi_epi16
_mm_unpackhi_epi8
_mm_unpacklo_epi16
_mm_unpacklo_epi64
_mm_unpacklo_epi8
_mm_xor_si128
