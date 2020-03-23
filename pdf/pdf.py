from reportlab.lib.pagesizes import A4
from reportlab.lib.units import mm
from reportlab.platypus import SimpleDocTemplate, Frame, PageTemplate, NextPageTemplate, PageBreak

from navi import Navi

import json

PAGE_WIDTH, PAGE_HEIGHT = A4


def get_data():
    f = open('data.json', encoding='utf-8')
    data = f.read()
    f.close()
    return data


def chunks(l, n):
    for i in range(0, len(l), n):
        yield l[i:i + n]


def generate_navis(data):
    navis = []
    for d in data:
        navis += [Navi(d['icon'], d['zone'], d['title'], d['category']) for i in range(d['quantity'])]
    result = []
    for c in chunks(navis, 21):
        result += c + [NextPageTemplate('ThreeCols'), PageBreak()]
    return result


def generate_frames():
    frame_w, frame_h = 60*mm, 280*mm
    result = []
    for i in range(3):
        result.append(
            Frame(10*mm + frame_w*i, PAGE_HEIGHT - frame_h - 10*mm, frame_w, frame_h, showBoundary=0,
                  topPadding=0, rightPadding=0, bottomPadding=0, leftPadding=0)
        )
    return result


def create_pdf(data):
    d = json.loads(data)
    doc = SimpleDocTemplate('test.pdf', pagesize=A4, setTitle='Тест',
                            topMargin=10*mm, rightMargin=10*mm, bottomMargin=10*mm, leftMargin=10*mm)
    doc.addPageTemplates(PageTemplate(id='ThreeCols', frames=generate_frames()))
    doc.build(generate_navis(d))


if __name__ == '__main__':
    create_pdf(get_data())
