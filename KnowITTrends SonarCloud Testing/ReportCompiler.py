from ReportWriter import ReportWriter
from CloudStorage import CloudStorage
from StatisticalPrediction import StatisticalPrediction
import uuid
from fpdf import FPDF
from PIL import Image

class ReportCompiler:
    _report_writer = ReportWriter()
    _cloud_storage = CloudStorage()
    _statistical_prediction = StatisticalPrediction()

    def __init__(self):
        pass

    def writeMarkdownText(self, pdf, text, line_height=8):
        """
        Splits the text on '**' markers and writes text to the PDF.
        Text between ** markers is rendered in bold.
        """
        #pdf.add_font("DejaVu", "", "font/dejavu-sans/ttf/DejaVuSans.ttf", uni=True)
        for line in text.split("\n"):
            parts = line.split("**")
            for i, part in enumerate(parts):
                font_style = "B" if i % 2 == 1 else ""
                pdf.set_font("DejaVu", font_style, 8)
                pdf.write(line_height, part)
            pdf.ln(line_height)

    def addFonts(self, pdf: FPDF):
        pdf.add_font(family="DejaVu", fname="DejaVuSans.ttf", uni=True)
        pdf.add_font(family="DejaVu", style="B", fname="font/dejavu-sans/ttf/DejaVuSans-Bold.ttf", uni=True)
        pdf.add_font(family="DejaVu", style="O", fname="font/dejavu-sans/ttf/DejaVuSans-Oblique.ttf", uni=True)

    def getTextPrediction(self, 
                          report_type: str, 
                          type_id: str,
                            overview_forex: bool = True,
                            key_figures_forex: bool = True,
                            recent_performance_forex: bool = True,
                            future_outlook_forex: bool = True,
                            forecast_forex: bool = True,
                            introduction_country: bool = True,
                            historic_economic_performance_country: bool = True,
                            historic_social_data_country: bool = True,
                            historic_environmental_data_country: bool = True,
                            future_economic_outlook_country: bool = True,
                            forecast_country: bool = True,
                            commodity_overview_commodity: bool = True,
                            historic_price_analysis_commodity: bool = True,
                            recent_price_trends_commodity: bool = True,
                            future_outlook_commodity: bool = True,
                            forecast_commodity: bool = True):

        # Get AI text prediction
        if report_type == "commodity":
            text_prediction = self._report_writer.WriteCommodityReport(commodity_id=type_id, 
                                                                       commodity_overview=commodity_overview_commodity,
                                                                       historic_price_analysis=historic_price_analysis_commodity,
                                                                       recent_price_trends=recent_price_trends_commodity, 
                                                                       future_outlook=future_outlook_commodity, 
                                                                       forecast=forecast_commodity)
        elif report_type == "country":
            text_prediction = self._report_writer.WriteCountryReport(country_code=type_id, 
                                                                     introduction=introduction_country, 
                                                                     historic_economic_performance=historic_economic_performance_country, 
                                                                     historic_social_data=historic_social_data_country, 
                                                                     historic_environmental_data=historic_environmental_data_country, 
                                                                     future_economic_outlook=future_economic_outlook_country, 
                                                                     forecast=forecast_country)
        elif report_type == "forex":
            base = type_id[:3]
            quote = type_id[-3:]
            text_prediction = self._report_writer.WriteForexReport(base=base, 
                                                                   quote=quote, 
                                                                   overview=overview_forex, 
                                                                   key_figures=key_figures_forex, 
                                                                   recent_performance=recent_performance_forex, 
                                                                   future_outlook=future_outlook_forex, 
                                                                   forecast=forecast_forex)
        else:
            text_prediction = {"Error": "No prediction received."}
        return text_prediction

    def CompilePDF(self, 
                   data: dict, 
                   report_type: str, 
                   type_id: str, 
                   interval: str,
                    overview_forex: bool = True,
                    key_figures_forex: bool = True,
                    recent_performance_forex: bool = True,
                    future_outlook_forex: bool = True,
                    forecast_forex: bool = True,
                    introduction_country: bool = True,
                    historic_economic_performance_country: bool = True,
                    historic_social_data_country: bool = True,
                    historic_environmental_data_country: bool = True,
                    future_economic_outlook_country: bool = True,
                    forecast_country: bool = True,
                    commodity_overview_commodity: bool = True,
                    historic_price_analysis_commodity: bool = True,
                    recent_price_trends_commodity: bool = True,
                    future_outlook_commodity: bool = True,
                    forecast_commodity: bool = True):
    
        text_prediction = self.getTextPrediction(report_type=report_type, type_id=type_id, 
                                                 overview_forex=overview_forex, 
                                                 key_figures_forex=key_figures_forex, 
                                                 recent_performance_forex=recent_performance_forex, 
                                                 future_outlook_forex=future_outlook_forex,
                                                 forecast_forex=forecast_forex,
                                                 introduction_country=introduction_country,
                                                 historic_economic_performance_country=historic_economic_performance_country,
                                                 historic_social_data_country=historic_social_data_country,
                                                 historic_environmental_data_country=historic_environmental_data_country,
                                                 future_economic_outlook_country=future_economic_outlook_country,
                                                 forecast_country=forecast_country,
                                                 commodity_overview_commodity=commodity_overview_commodity,
                                                 historic_price_analysis_commodity=historic_price_analysis_commodity,
                                                 recent_price_trends_commodity=recent_price_trends_commodity,
                                                 future_outlook_commodity=future_outlook_commodity,
                                                 forecast_commodity=forecast_commodity
                                                 )
        
        fig_name = uuid.uuid4().hex
        pdf_name = uuid.uuid4().hex

        include_image = False
        
        # Create the PNG forecast image if forecast is selected

        if report_type == "forex":
            if forecast_forex == True:
                self._statistical_prediction.CreatePNG(datapoints=data, png_name=fig_name, interval=interval)
                include_image = True
        if report_type == "country":
            if forecast_country == True:
                self._statistical_prediction.CreatePNG(datapoints=data, png_name=fig_name, interval=interval)
                include_image = True
        if report_type == "commodity":
            if forecast_commodity == True:
                self._statistical_prediction.CreatePNG(datapoints=data, png_name=fig_name, interval=interval)
                include_image = True

        # Create PDF
        pdf = FPDF()
        pdf.add_page()

        # Add header text
        self.addFonts(pdf=pdf)
        
        pdf.set_font("DejaVu", "B", 12)
        pdf.cell(0, 10, "Trends - Forecast Report", ln=True, align="C")
        pdf.set_font("DejaVu", "", 12)

        # Add descriptive text with markdown formatting (bold text between ** markers)
        self.writeMarkdownText(pdf, text_prediction)
        #pdf.write(text_prediction)

        if include_image == True:

            # Optionally, you can determine the position and scaling of the image.
            # Here we insert the image starting 10mm below the last written text:
            current_y = pdf.get_y() + 10
            margin = 10
            max_width = pdf.w - 2 * margin

            # Use Pillow to get the image dimensions (in pixels)
            img = Image.open(f"temp/{fig_name}.png")
            img_width_px, img_height_px = img.size

            # Convert pixels to millimeters (assuming 96 dpi)
            dpi = 96.0
            img_width_mm = img_width_px * 25.4 / dpi
            img_height_mm = img_height_px * 25.4 / dpi

            # Scale image if wider than available width
            if img_width_mm > max_width:
                scale = max_width / img_width_mm
                img_width_mm = max_width
                img_height_mm *= scale

            # Check available vertical space, add new page if necessary
            available_height = pdf.h - current_y - margin
            if img_height_mm > available_height:
                pdf.add_page()
                current_y = margin

        # Insert the image into the PDF if forecast is selected
            pdf.image(f"temp/{fig_name}.png", x=margin, y=current_y, w=img_width_mm)

        self.add_disclaimer(pdf=pdf)

        # Save the PDF to a file
        pdf.output(f"temp/{pdf_name}.pdf")

        return self.UploadPDF(pdf_file=f"temp/{pdf_name}.pdf", pdf_name=pdf_name)
        
    def UploadPDF(self, pdf_file, pdf_name):
        return self._cloud_storage.UploadFile(file_content=pdf_file, file_name=f"temp/{pdf_name}")

    def add_rights(self, pdf:FPDF):
        pdf.set_y(-35)
        pdf.set_font("DejaVu", "O", 8)
        pdf.cell(0, 10, "© 2025 BlueBananaBrand, Inc.  All Rights Reserved.", ln=True, align="C")
    
    def add_disclaimer(self, pdf):
        pdf.set_y(-35)
        pdf.set_font("DejaVu", "O", 8)
        disclaimer = "This report should not be used for anything and is not financial advice."
        pdf.cell(0, 10, disclaimer, ln=True, align="C")

