from reportlab.lib.units import mm
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.colors import Color
from reportlab.platypus import Flowable, Frame, Image, Paragraph, KeepInFrame, Table, TableStyle
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont

pdfmetrics.registerFont(TTFont('OfficinaSans', 'fonts/OfficinaSansBookC.ttf'))
pdfmetrics.registerFont(TTFont('OfficinaSerifBold', 'fonts/OfficinaSerifC-Bold.ttf'))


class Navi(Flowable):
    def __init__(self, icon, zone, title, category):
        Flowable.__init__(self)
        self.width = 60*mm
        self.height = 40*mm
        self.icon = icon
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
        self.draw_icon_frame()
        self.draw_zone_frame()

    def draw_icon_frame(self):
        self.canv.saveState()
        self.canv.setFillColorRGB(0, 0, 0)
        icon_frame = Frame(3 * mm, 40 * mm - 1.5 * mm - 7 * mm, 7 * mm, 7 * mm, showBoundary=0,
                           topPadding=0, rightPadding=0, bottomPadding=0, leftPadding=0)
        icon = Image(self.icon, 7 * mm, 7 * mm)
        icon_frame.addFromList([icon], self.canv)
        self.canv.restoreState()

    def draw_zone_frame(self):
        self.canv.saveState()
        offset = self.calc_zone_offset()
        leading = 11.1 if len(self.zone) > 16 else 11
        style = ParagraphStyle(name='zone', fontSize=15, fontName='OfficinaSerifBold', textColor=Color(1, 1, 1, 1),
                               alignment=1, leading=leading, splitLongWords=False, spaceShrinkage=0)
        zone_frame = Frame(12*mm + offset, 40*mm - 1.5*mm - 7*mm, 45*mm, 7*mm, showBoundary=0,
                           topPadding=0, rightPadding=0, bottomPadding=0, leftPadding=0)
        zone = Paragraph(self.zone, style)
        keep = KeepInFrame(45*mm, 7*mm, [zone], hAlign='CENTER', vAlign='MIDDLE', fakeWidth=False)
        zone_frame.addFromList([keep], self.canv)
        self.canv.restoreState()

    def calc_zone_offset(self):
        n = len(self.zone)
        return (n - 13) / 4 if n < 10 else 0
