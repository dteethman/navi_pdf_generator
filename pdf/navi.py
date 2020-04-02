from reportlab.lib.units import mm
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.colors import Color
from reportlab.platypus import Flowable, Frame, Image, Paragraph, KeepInFrame, Table, TableStyle
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont

import pdf.words as words

pdfmetrics.registerFont(TTFont('OfficinaSans', 'pdf/fonts/OfficinaSansBookC.ttf'))
pdfmetrics.registerFont(TTFont('OfficinaSerifBold', 'pdf/fonts/OfficinaSerifC-Bold.ttf'))


class Navi(Flowable):
    def __init__(self, icon, zone, title, category):
        Flowable.__init__(self)
        self.width = 60*mm
        self.height = 40*mm
        self.icon = 'pdf/icons/' + icon
        self.zone = zone
        if title == '':
            self.title, self.category = category, title
        else:
            self.title = title
            self.category = category

    def draw(self):
        # Рамки ценников
        self.canv.setLineWidth(.25)
        self.canv.setStrokeColorRGB(.78, .78, .78)
        self.canv.rect(0, 0, self.width, self.height)

        # Верхняя плашка
        self.canv.rect(0, 40 * mm - 10 * mm, self.width, 10 * mm, fill=1, stroke=0)

        # Контент
        self.draw_icon()
        self.draw_zone()
        self.draw_category()
        self.draw_title()

    def draw_icon(self):
        self.canv.saveState()
        self.canv.setFillColorRGB(0, 0, 0)
        icon_frame = Frame(3 * mm, 40 * mm - 1.5 * mm - 7 * mm, 7 * mm, 7 * mm, showBoundary=0,
                           topPadding=0, rightPadding=0, bottomPadding=0, leftPadding=0)
        icon = Image(self.icon, 7 * mm, 7 * mm)
        icon_frame.addFromList([icon], self.canv)
        self.canv.restoreState()

    def draw_zone(self):
        self.canv.saveState()
        offset = 9*mm if len(self.zone) < 10 else 0
        width = 54*mm if len(self.zone) < 10 else 45*mm
        leading = 11.1 if len(self.zone) > 16 else 11
        style = ParagraphStyle(name='zone', fontSize=15, fontName='OfficinaSerifBold', textColor=Color(1, 1, 1, 1),
                               alignment=1, leading=leading, splitLongWords=False, spaceShrinkage=0)
        zone_frame = Frame(12*mm - offset, 40*mm - 1.5*mm - 7*mm, width, 7*mm, showBoundary=0,
                           topPadding=0, rightPadding=0, bottomPadding=0, leftPadding=0)
        zone = Paragraph(self.zone, style)
        keep = KeepInFrame(width, 7*mm, [zone], hAlign='CENTER', vAlign='MIDDLE', fakeWidth=False)
        zone_frame.addFromList([keep], self.canv)
        self.canv.restoreState()

    def draw_title(self):
        self.canv.saveState()

        fsize, flead, offset = words.get_font_settings(len(self.title))
        if self.category == '':
            offset = offset + 2*mm if '<br/>' not in self.title else 3
        elif '<br/>' not in self.title:
            offset = offset
        else:
            offset = 0

        title = words.rebuild_lines(self.title)
        style = ParagraphStyle(name='category', fontSize=fsize, fontName='OfficinaSans', textColor=Color(0, 0, 0, 1),
                               alignment=1, leading=flead, splitLongWords=False, spaceShrinkage=0)
        title_frame = Frame(3*mm, 12*mm - offset, 54*mm, 16*mm, showBoundary=0,
                            topPadding=0, rightPadding=0, bottomPadding=0, leftPadding=0)
        title_p = Paragraph(title, style)
        keep = KeepInFrame(54*mm, 16*mm, [title_p], hAlign='CENTER', vAlign='MIDDLE', fakeWidth=False)
        title_frame.addFromList([keep], self.canv)
        self.canv.restoreState()

    def draw_category(self):
        self.canv.saveState()
        style = ParagraphStyle(name='category', fontSize=12, fontName='OfficinaSans', textColor=Color(0, 0, 0, 1),
                               alignment=1, leading=12, splitLongWords=False, spaceShrinkage=0)
        category_frame = Frame(3*mm, 3*mm, 54*mm, 5*mm, showBoundary=0,
                               topPadding=0, rightPadding=0, bottomPadding=0, leftPadding=0)
        category = Paragraph(self.category, style)
        keep = KeepInFrame(54*mm, 5*mm, [category], hAlign='CENTER', vAlign='BOTTOM', fakeWidth=False)
        category_frame.addFromList([keep], self.canv)
        self.canv.restoreState()
