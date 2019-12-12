from math import pi, radians, cos, sin, tan, atan
import numpy as np

sqr = 0
ang = 45


def m_q_from_apt(p0, p1):
    assert p0[0] != p1[0], "points should not be aligned vertically!"
    m = (p1[1] - p0[1]) / (p1[0] - p0[0])
    return m, -m * p0[0] + p0[1]


def m_q_from_ang(p0, ang):
    assert ang != 90 or ang != 270, "ang should be different than 90 or 270"
    m = tan(ang)
    return m, -m * p0[0] + p0[1]


def line_intersection(m1, q1, m2, q2):
    A = np.array([[m1, -1], [m2, -1]])
    B = np.array([-q1, -q2])
    C = np.linalg.solve(A, B)
    return tuple(C)


def interpolate_points(p1, p2, f):
    return tuple([p1[i] + (p2[i] - p1[i]) * f for i in (0, 1)])


def make_anticlockwise(cnt):
    if cnt.clockwise == "True" or cnt.clockwise == True:
        cnt.reverse()


def contour_operations(cnt, trs, rot):
    # Applying transformations
    cnt.rotateBy(rot)
    cnt.moveBy(trs)
    # Setting the contour correctly
    make_anticlockwise(cnt)
    cnt.round()
    cnt.changed()


def rect(gly, box, rot, mrr, tck=100):
    opt = box[0] + box[2] / 2, box[1] + box[3] / 2
    hgt = box[3] / 2
    if rot % 90 == 0:
        hgt = box[2] / 2
    # Points
    p0 = -tck / 2, tck / 2
    p1 = tck / 2, tck / 2
    p2 = tck / 2, -hgt
    p3 = -tck / 2, -hgt
    # Drawing
    pen = gly.getPen()
    pen.moveTo(p0)
    for p in [p1, p2, p3]:
        pen.lineTo(p)
    pen.closePath()
    # Fixing contour
    cnt = gly[-1]
    contour_operations(cnt=cnt, trs=opt, rot=rot)


def __diag(gly, box, tck, rot, mrr, prp):
    wdt, hgt = box[2], box[3]

    pt0 = box[0] + box[2] / 2, box[1]
    pt1 = pt0[0] + box[2] / 2, pt0[1] + box[3] / 2
    # Converting to radians
    ang = prp["ang"]
    ang = radians(ang)
    # Calcolo angolo manipolatore dipendente
    xI = hgt / (tan(pi / 2 - ang) + hgt / wdt)
    yI = tan(pi / 2 - ang) * xI
    ang_dip = atan((yI - hgt) / (xI - wdt)) + pi / 2
    # Points 0 - Shortcuts
    tck_cos = tck / 2 * cos(ang)
    tck_sin = tck / 2 * sin(ang)
    # Points 0
    pt0A = pt0[0] + tck_cos, pt0[1] - tck_sin
    pt0B = pt0[0] - tck_cos, pt0[1] + tck_sin
    # Points 1 - Shortcuts
    tck_cos = tck / 2 * cos(ang_dip)
    tck_sin = tck / 2 * sin(ang_dip)
    # Points 1
    pt1A = pt1[0] - tck_cos, pt1[1] - tck_sin
    pt1B = pt1[0] + tck_cos, pt1[1] + tck_sin


def diag(gly, box, tck, rot, mrr, prp):
    wdt, hgt = box[2], box[3]
    ang = prp["ang"]
    sqr = prp["sqr"]
    mid = prp["mid"]
    pt0 = box[0] + box[2] / 2, box[1]
    pt1 = pt0[0] + box[2] / 2, pt0[1] + box[3] / 2
    # Converting to radians
    ang = radians(ang)
    # Calcolo angolo manipolatore dipendente
    xI = hgt / (tan(pi / 2 - ang) + hgt / wdt)
    yI = tan(pi / 2 - ang) * xI
    ang_dip = atan((yI - hgt) / (xI - wdt)) + pi / 2
    # Points 0 - Shortcuts
    tck_cos = tck / 2 * cos(ang)
    tck_sin = tck / 2 * sin(ang)
    # Points 0
    pt0A = pt0[0] + tck_cos, pt0[1] - tck_sin
    pt0B = pt0[0] - tck_cos, pt0[1] + tck_sin
    # Points 1 - Shortcuts
    tck_cos = tck / 2 * cos(ang_dip)
    tck_sin = tck / 2 * sin(ang_dip)
    # Points 1
    pt1A = pt1[0] - tck_cos, pt1[1] - tck_sin
    pt1B = pt1[0] + tck_cos, pt1[1] + tck_sin
    # Point MAX A
    if pi / 2 - ang != ang_dip - pi / 2:
        m0, q0 = m_q_from_ang(pt0A, pi / 2 - ang)
        m1, q1 = m_q_from_ang(pt1A, ang_dip - pi / 2)
        ptMA = line_intersection(m0, q0, m1, q1)
    else:
        ptMA = interpolate_points(pt0A, pt1A, .5)
    # Point MAX B
    if pi / 2 - ang != ang_dip - pi / 2:
        m0, q0 = m_q_from_ang(pt0B, pi / 2 - ang)
        m1, q1 = m_q_from_ang(pt1B, ang_dip - pi / 2)
        ptMB = line_intersection(m0, q0, m1, q1)
    else:
        ptMB = interpolate_points(pt0B, pt1B, .5)
    # Point CONTROL A
    pt0AC = interpolate_points(pt0A, ptMA, sqr)
    pt1AC = interpolate_points(pt1A, ptMA, sqr)
    # Point CONTROL B
    pt0BC = interpolate_points(pt0B, ptMB, sqr)
    pt1BC = interpolate_points(pt1B, ptMB, sqr)
    # t
    pen = gly.getPen()
    pen.moveTo(pt0A)
    pen.curveTo(pt0AC, pt1AC, pt1A)
    pen.lineTo(pt1B)
    pen.curveTo(pt1BC, pt0BC, pt0B)
    pen.closePath()
    # Fixing contour
    cnt = gly[-1]
    if mid == True:
        cnt.scaleBy((-1, 1), origin=(box[0] + box[2] / 4 * 3, box[1] + box[3] / 4))
    if mrr == True:
        cnt.scaleBy((-1, 1), origin=(box[0] + box[2] / 2, box[1] + box[3] / 2))
    cnt.rotateBy(rot, origin=(box[0] + box[2] / 2, box[1] + box[3] / 2))
    contour_operations(cnt=cnt, trs=(0, 0), rot=0)


def diag_0(gly, box, rot, mrr, tck=100):
    prp = {"mid": False, "ang": ang, "sqr": sqr}
    diag(gly, box, tck, rot, mrr, prp)


def diag_1(gly, box, rot, mrr, tck=100):
    prp = {"mid": True, "ang": ang, "sqr": sqr}
    diag(gly, box, tck, rot, mrr, prp)
