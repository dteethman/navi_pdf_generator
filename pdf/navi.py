from reportlab.lib.units import mm
from reportlab.platypus import Flowable
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont

pdfmetrics.registerFont(TTFont('OfficinaSans', 'fonts/OfficinaSansBookC.ttf'))
pdfmetrics.registerFont(TTFont('OfficinaSerifBold', 'fonts/OfficinaSerifC-Bold.ttf'))


class Navi(Flowable):
    def __init__(self, zone, title, category):
        Flowable.__init__(self)
        self.width = 60*mm
        self.height = 40*mm
        self.zone = zone
        self.title = title
        self.category = category

    def draw(self):
        self.canv.setLineWidth(.25)
        self.canv.setStrokeColorRGB(.78, .78, .78)
        self.canv.rect(0, 0, self.width, self.height)
        self.canv.setFont('OfficinaSerifBold', 12)
        self.canv.drawString(3*mm, 38*mm - 12, self.zone)
        self.canv.drawString(3*mm, 38*mm - 24, self.title)
        self.canv.drawString(3*mm, 38*mm - 36, self.category)
