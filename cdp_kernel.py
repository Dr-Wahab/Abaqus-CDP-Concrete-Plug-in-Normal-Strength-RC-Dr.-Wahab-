# -*- coding: mbcs -*-
from __future__ import division
from math import exp, sqrt
from abaqus import mdb
from abaqusConstants import OFF

KEEP_RATIO = 0.8

def _downsample_pairs(pairs, keep_ratio=KEEP_RATIO):
    n = len(pairs)
    if n <= 2:
        return tuple(pairs)
    k = int(round(n * keep_ratio))
    if k < 2: k = 2
    idx = [0]
    if k > 2:
        for j in range(1, k-1):
            val = int(round(j * (n-1.0)/(k-1.0)))
            if val <= idx[-1]:
                val = min(idx[-1]+1, n-2)
            idx.append(val)
    idx.append(n-1)
    keep = []
    seen = set()
    for i in idx:
        if i not in seen:
            seen.add(i); keep.append(pairs[i])
    if len(keep) < 2:
        keep = [pairs[0], pairs[-1]]
    return tuple(keep)

def roundList(lst, precision):
    return [round(x, precision) for x in lst]

def tensile_strength_from(fc, law, ft_custom):
    fc = float(fc)
    law = str(law)
    if law == 'EC2' or law == 'fib2010':
        fcm = fc + 8.0
        return 0.30 * (fcm ** (2.0/3.0))
    elif law == 'ACI_SPLIT':
        return 0.56 * sqrt(fc)
    elif law == 'ACI_RUPTURE':
        return 0.62 * sqrt(fc)
    elif law == 'CUSTOM':
        return float(ft_custom)
    else:
        return 0.30 * ((fc + 8.0) ** (2.0/3.0))

def Concrete(f_c, form, meu, density, dil, exc, fb0_fc0, kshape, visc, tr, cr, tensionlaw, ft_custom):
    CompressionForm = form
    elim = 1 - exp(-f_c / 80.)
    if elim > 0.4: elim = 0.4

    a = 3.5 * (12.4 - 0.0166 * f_c) ** (-0.46)
    b = 0.83 * exp(-911. / f_c)
    Ec = 3320. * f_c ** 0.5 + 6900.
    r = f_c / 17. + 0.8
    e_c = f_c / Ec * r / (r - 1)
    Esec = f_c / e_c
    n1 = (1.02 - 1.17 * (Esec / Ec)) ** (-0.74)
    n2 = n1 + (a + 28. * b)

    e_c0 = elim * f_c / Ec
    Sf = tensile_strength_from(f_c, tensionlaw, ft_custom)

    e_ct = Sf / Ec
    ecut = 10 * e_ct

    frac = 5.
    strainc = [x * (e_c - e_c0) / frac for x in range(26)]

    if CompressionForm == 'Carreeira':
        stressc = [f_c * n1 * ((strainc[x] + e_c0) / e_c) / (n1 - 1 + ((strainc[x] + e_c0) / e_c) ** n1) if x <= frac else f_c * n2 * ((strainc[x] + e_c0) / e_c) / (n2 - 1 + ((strainc[x] + e_c0) / e_c) ** n2) for x in range(26)]
    elif CompressionForm == 'Madrid':
        stressc = [Ec * (strainc[x] + e_c0) * (1 - 0.5 * (strainc[x] + e_c0) / e_c) for x in range(26)]
    elif CompressionForm == 'SN1992':
        k = 1.05 * Ec * e_c / f_c
        stressc = [f_c * (k * ((strainc[x] + e_c0) / e_c) - ((strainc[x] + e_c0) / e_c) ** 2) / (1 + (k - 2) * (strainc[x] + e_c0) / e_c) for x in range(26)]
    elif CompressionForm == 'Majewski':
        k = f_c * (elim - 2) ** 2 / (elim - 1)
        stressc = [k * (strainc[x] + e_c0) ** 2 / (4 * e_c ** 2) - k * (strainc[x] + e_c0) / (2 * e_c) + f_c * elim ** 2 / (4 * elim - 4) for x in range(26)]
    else:
        stressc = [0.0 for _ in range(26)]

    dc = [1 - stressc[x] / f_c if (strainc[x] + e_c0) > e_c else 0.0 for x in range(26)]

    straint = [x * e_ct for x in range(20)]
    stresst = [Sf * (e_ct / (straint[x] + e_ct)) ** 0.85 for x in range(20)]
    dt = [1 - stresst[x] / Sf if (straint[x]) > 0.0 else 0.0 for x in range(20)]

    CompreB = tuple(zip(roundList(stressc, 5), roundList(strainc, 5)))
    CompreD = tuple(zip(roundList(dc, 5), roundList(strainc, 5)))
    TensioB = tuple(zip(roundList(stresst, 5), roundList(straint, 5)))
    TensioD = tuple(zip(roundList(dt, 5), roundList(straint, 5)))
    A = [stresst[x] / Sf for x in range(len(stresst))]
    TenStif = tuple(zip(roundList(A, 5), roundList(straint, 5)))

    CompreB = _downsample_pairs(CompreB, KEEP_RATIO)
    CompreD = _downsample_pairs(CompreD, KEEP_RATIO)
    TensioB = _downsample_pairs(TensioB, KEEP_RATIO)
    TensioD = _downsample_pairs(TensioD, KEEP_RATIO)
    TenStif = _downsample_pairs(TenStif, KEEP_RATIO)

    return CompreB, CompreD, TensioB, TensioD, TenStif, round(Ec, 5), meu, density, dil, exc, fb0_fc0, kshape, visc, tr, cr

def runCDP(model='Model-1', matname='C30', form='Carreeira', fc=30.0,
           density=2.4e-9, meu=0.20, dil=36.0, exc=0.1, fb0fc0=1.16, kshape=0.667,
           visc=0.0, tr=0.5, cr=1.0, tensionlaw='EC2', ftcustom=2.0):

    CompreB, CompreD, TensioB, TensioD, TenStif, Ec, meu, density, dil, exc, fb0_fc0, K, visc, tr, cr = Concrete(
        f_c=fc, form=form, meu=meu, density=density, dil=dil, exc=exc,
        fb0_fc0=fb0fc0, kshape=kshape, visc=visc, tr=tr, cr=cr,
        tensionlaw=tensionlaw, ft_custom=ftcustom)

    matKey = '%s_CDP' % matname
    m = mdb.models[str(model)]
    m.Material(name=matKey)
    m.materials[matKey].Density(table=((density, ),  ))
    m.materials[matKey].Elastic(table=((Ec, meu),  ))
    m.materials[matKey].ConcreteDamagedPlasticity(table=((dil, exc, fb0_fc0, K, visc),  ))
    m.materials[matKey].concreteDamagedPlasticity.ConcreteCompressionHardening(rate=OFF, table=CompreB)
    m.materials[matKey].concreteDamagedPlasticity.ConcreteCompressionDamage(tensionRecovery=tr, table=CompreD)
    m.materials[matKey].concreteDamagedPlasticity.ConcreteTensionStiffening(rate=OFF, table=TensioB)
    m.materials[matKey].concreteDamagedPlasticity.ConcreteTensionDamage(compressionRecovery=cr, table=TensioD)

    print('CDP v1.2f: %s created (tension law=%s, fc=%.2f MPa)' % (matKey, tensionlaw, fc))
