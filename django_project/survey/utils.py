# import math
# import logging
# import os
# import shutil
# from datetime import datetime

# from django.contrib import messages
# from django.conf import settings
# from django.utils.crypto import get_random_string
# from django.core.files.storage import FileSystemStorage

# from PIL import Image
# from exif import Image as ImageSource
# from djmoney.money import Money
# from rolepermissions.roles import get_user_roles, RolesManager

# from reportlab.lib import colors
# from reportlab.lib.units import inch
# from reportlab.pdfbase import pdfmetrics
# from reportlab.pdfbase.ttfonts import TTFont
# from reportlab.lib.pagesizes import A4, landscape
# from reportlab.platypus import (
#     Spacer,
#     Table,
#     Paragraph,
#     SimpleDocTemplate,
# )

# from tralard.constants import BASE_TEMP_DIR

# logger = logging.getLogger(__name__)


# def unique_slugify(instance, slug):
#     """
#     Generate slug and ensure it is unique,

#     Parameters
#     ----------
#     instance : (django.db.models.Mode) This is a model instance the slug is generated for.
#     slug : (string) a unique string that serves as a unique id for the object.

#     Returns
#     -------
#     slug: (string): a unique string of type slug.
#     i.e >>> 'project-tralard-unique-entry-1245-live'

#     """
#     model = instance.__class__
#     unique_slug = slug
#     while model.objects.filter(slug=unique_slug).exists():
#         unique_slug = slug + get_random_string(length=4)
#     return unique_slug


# def compute_total_amount(model_name, object_id: int, action: str) -> Money:
#     """
#     Compute the total amount of either disburesment or expenditure.

#     Parameters
#     ----------
#     model_name : Model.model
#         The model name.
#     object_id : int
#         The object id.
#     action : str
#         The action to be performed, either disburesment or expenditure.

#     Returns
#     -------
#     float
#         The total amount.

#     """
#     all_amount_values = []
#     if action.lower() == "disbursement":
#         all_amount_objects = model_name.objects.filter(fund__id=object_id)
#     elif action.lower() == "expenditure":
#         all_amount_objects = model_name.objects.filter(disbursment__id=object_id)

#     for amount in all_amount_objects:
#         amount_value = amount.amount
#         all_amount_values.append(amount_value)
#     total_amount = sum(all_amount_values)
#     return total_amount


# def get_balance(initial_amount: float, total_amount: float) -> Money:
#     """
#     Get the balance of the fund.

#     Parameters
#     ----------
#     initial_amount : float
#         The initial amount of the fund.

#     total_amount : float
#         The total amount of the disbursement.
#     """
#     difference = initial_amount - total_amount
#     return difference


# def check_requested_deduction_against_balance(
#         balance, requested_amount, requested_semantic, balance_semantic
# ) -> Money:
#     """
#     Check if the requested amount is greater than the balance.

#     Parameters
#     ----------
#     balance : float
#         The balance of the fund or disbursment.

#     requested_amount : float
#         The requested amount.

#     requested_semantic : str
#         The requested semantic.

#     balance_semantic : str
#         The balance semantic.

#     Returns
#     -------
#     float
#     """
#     if requested_amount > balance:
#         raise ValueError(
#             f"Requested {requested_semantic} amount can not be more than the remaining {balance_semantic} balance."
#         )
#     return requested_amount


# def get_available_roles():
#     uncleaned_user_roles = RolesManager.get_roles()
#     cleaned_user_roles = []

#     for role in uncleaned_user_roles:
#         cleaned_user_roles.append(role.get_name())
#     user_roles = [
#         role_name.replace("_", " ").title() for role_name in cleaned_user_roles
#     ]
#     return user_roles


# def current_user_roles(user):
#     uncleaned_user_roles = get_user_roles(user)
#     cleaned_user_roles = []

#     for role in uncleaned_user_roles:
#         cleaned_user_roles.append(role.get_name())
#     user_roles = [
#         role_name.replace("_", " ").title() for role_name in cleaned_user_roles
#     ]
#     return user_roles


# def user_profile_update_form(user):
#     try:
#         from tralard.forms.profile import ProfileForm  # don't move this import on top
#     except:
#         pass
#     user_create_form = ProfileForm(instance=user)
#     return user_create_form


# def new_user_create_form():
#     try:
#         from authentication.forms import SignUpForm
#     except:
#         pass
#     user_update_form = SignUpForm()
#     return user_update_form


# def user_update_form(instance):
#     try:
#         from authentication.forms import UserUpdateForm
#     except:
#         pass
#     user_update_form = UserUpdateForm(instance=instance)
#     return user_update_form


# def all_users():
#     try:
#         from django.contrib.auth.models import User  # don't move this import on top
#     except:
#         pass
#     available_user_list = User.objects.all()
#     return available_user_list


# def training_update_form(training):
#     try:
#         from tralard.forms.training import TrainingForm  # don't move this import on top
#     except:
#         pass
#     training_update_form = TrainingForm(instance=training)
#     return training_update_form


# class IndicatorReportBuild(SimpleDocTemplate):
#     def __init__(self, filename, indicators, **kwargs):
#         super().__init__(filename, pagesize=landscape(A4), **kwargs)
#         self.leftMargin = 30
#         self.rightMargin = 30
#         self.doc_elements = [
#             Spacer(1, 2 * inch),
#             Spacer(1, 2 * inch),
#             Spacer(1, 2 * inch),
#         ]
#         self.indicators = indicators
#         self.assets_root = settings.STATIC_ROOT + "/assets"

#         pdfmetrics.registerFont(
#             TTFont("roboto-bold", f"{self.assets_root}/fonts/Roboto/Roboto-Bold.ttf")
#         )
#         pdfmetrics.registerFont(
#             TTFont(
#                 "roboto-regular", f"{self.assets_root}/fonts/Roboto/Roboto-Regular.ttf"
#             )
#         )
#         pdfmetrics.registerFont(
#             TTFont(
#                 "roboto-medium", f"{self.assets_root}/fonts/Roboto/Roboto-Medium.ttf"
#             )
#         )

#     def build_doc(self):
#         data, row_column_spans, actual_values_row_colorfills = self.create_table_rows()
#         style = [
#             ("GRID", (0, 0), (-1, -1), 0.7, colors.black),
#             ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
#             ("ALIGN", (0, 0), (-1, -1), "CENTER"),
#             (
#                 "BACKGROUND",
#                 (0, 0),
#                 (-1, 0),
#                 colors.Color(red=(179.0 / 255), green=(231.0 / 255), blue=(115 / 255)),
#             ),
#         ]

#         for row_to_fillcolor in actual_values_row_colorfills:
#             style.append(row_to_fillcolor)

#         for _tuple in row_column_spans:
#             style.append(_tuple)

#         t = Table(
#             data,
#             style=style,
#             colWidths=[115, 140, 70, 50, 60, 60, 60, 60, 60],
#             repeatRows=1,
#         )
#         self.doc_elements.append(t)

#         self.build(
#             self.doc_elements, onFirstPage=self.firstPage, onLaterPages=self.laterPages
#         )

#     def firstPage(self, canvas, doc):
#         """
#         Defines the fixed features of the first page of the document.
#         """
#         datestamp = datetime.today().strftime("%d %b %Y")

#         canvas.saveState()
#         canvas.setTitle(f"Think2044 Indicator Report | {datestamp}")

#         canvas.drawImage(
#             f"{self.assets_root}/images/logos/mgee_logo.jpeg",
#             400,
#             480,
#             width=75,
#             height=75,
#         )
#         canvas.drawImage(
#             f"{self.assets_root}/images/partners/cif.png",
#             170,
#             175,
#             width=115,
#             height=80,
#             mask="auto",
#         )
#         canvas.drawImage(
#             f"{self.assets_root}/images/partners/adb.png",
#             315,
#             165,
#             width=100,
#             height=90,
#             mask="auto",
#         )
#         canvas.drawImage(
#             f"{self.assets_root}/images/logos/logo.png", 460, 170, width=90, height=90
#         )
#         canvas.drawImage(
#             f"{self.assets_root}/images/partners/zima.png",
#             600,
#             170,
#             width=90,
#             height=90,
#             mask="auto",
#         )
#         canvas.drawImage(
#             f"{self.assets_root}/images/partners/wbg.png",
#             320,
#             100,
#             width=270,
#             height=50,
#             mask="auto",
#         )

#         canvas.setFont("roboto-bold", 20)
#         canvas.drawCentredString(420, 460, "MINISTRY OF GREEN ECONOMY AND ENVIRONMENT")

#         canvas.setFont("roboto-medium", 15)
#         canvas.drawCentredString(420, 430, "NATIONAL PROJECT COORDINATING UNIT")

#         canvas.setFont("roboto-medium", 12)
#         canvas.drawCentredString(
#             420, 410, "TRANSFORMING LANDSCAPES FOR RESILIENCE AND DEVELOPMENT"
#         )

#         canvas.setFont("roboto-medium", 25)
#         canvas.drawCentredString(420, 330, "Report For Indicator Results")
#         canvas.line(250, 320, 580, 320)

#         canvas.setFont("roboto-regular", 12)
#         canvas.drawString(50, 50, datestamp)

#         canvas.setFont("roboto-medium", 14)
#         canvas.setFillColorRGB(0.18, 0.47, 0)  # choose your font colour
#         canvas.drawString(650, 50, "Think2044.com")
#         hostlink = "http://think2044.com"
#         canvas.linkURL(hostlink, (650, 70, 750, 35), thickness=0)

#         canvas.restoreState()

#     def laterPages(self, canvas, doc):
#         """
#         Since we want pages after the first to look different from the first we define an alternate layout for the fixed
#         features of the other pages.
#         """
#         canvas.saveState()
#         canvas.setFont("Times-Roman", 9)
#         canvas.drawString(inch, 0.75 * inch, f"Page {doc.page}")
#         canvas.setFont("Times-Roman", 20)
#         canvas.restoreState()

#     def create_table_rows(self):
#         """
#         Generates lists dynamically for Indicators which are representations of table rows.
#         """
#         # This list is a represantation of table data. The pre-added items are table rows.
#         data = [
#             [
#                 Paragraph("<font size=13><b>Indicator</b></font>"),
#                 Paragraph("<font size=13><b>Unit of Measure</b></font>"),
#                 Paragraph("<font size=13><b>Baseline </b></font>"),
#                 "",
#                 Paragraph("<font size=13><b>Year 1</b></font>"),
#                 Paragraph("<font size=13><b>Year 2</b></font>"),
#                 Paragraph("<font size=13><b>Year 3</b></font>"),
#                 Paragraph("<font size=13><b>Year 4</b></font>"),
#                 Paragraph("<font size=13><b>Year 5</b></font>"),
#             ]
#         ]
#         row_column_spans = []
#         actual_values_row_colorfills = []

#         indicator_start_column = 0
#         indicator_start_row = 0
#         indicator_end_column = 0
#         indicator_end_row = 0
#         third_column_sc = 2
#         third_column_sr = 0
#         third_column_ec = 2
#         third_column_er = 0

#         # The following 4 values are used dynamically color('grey') each Indicator target row that contains 'Indicator actual data'.
#         actual_values_col_colorfill_start = 3
#         actual_values_row_colorfill_start = 2
#         actual_values_col_colorfill_end = -1
#         actual_values_row_colorfill_end = 2

#         iter_count = 0

#         current_year = datetime.now().year
#         for indicator_obj in self.indicators:
#             indicator_targets = indicator_obj.indicatortarget_set.all()
#             targets_count = indicator_targets.count()

#             # This 'row' will have column data such as Indicator name, description, Baseline ,Target, Year 1, Year 2,
#             # Year 3, Year 4, Year 5 The 'sub_row' is part of the row and will have column data like Unit of
#             # mearsure, Actual, and the rest of values for each year.
#             row = []
#             sub_row = ["", ""]

#             # These variables are to be used to style/set the span for the 'Indicator' column
#             indicator_start_row = indicator_end_row + 1
#             indicator_end_row = (targets_count * 2) + indicator_end_row

#             # Example of tuple: ('SPAN', (0, 1), (0, 2)) This is to be used to style each Indicator row in the table

#             if indicator_targets:
#                 row_column_spans.append(
#                     (
#                         "SPAN",
#                         (indicator_start_column, indicator_start_row),
#                         (indicator_end_column, indicator_end_row),
#                     )
#                 )
#                 for target in indicator_targets:
#                     row.append(
#                         Paragraph(indicator_obj.name)
#                     )  # Append Indicator name as first column)
#                     row.append(Paragraph(target.description))
#                     row.append(Paragraph(target.baseline_value))
#                     row.append(Paragraph("<b>Targets</b>"))
#                     try:
#                         sub_row.insert(1, Paragraph(f"<b>{target.unit_of_measure.unit_of_measure}</b>"))
#                     except AttributeError:
#                         sub_row.insert(1, Paragraph(""))

#                     sub_row.insert(3, Paragraph("<b>Actual</b>"))

#                     sub_row_count = 5

#                     # Get target values and actual values for each target in the
#                     # Indicator e.g 5000 - year(2022), 8000 - year(2023), 12000 - year(2024)
#                     for (yearly_target_value) in target.indicatortargetvalue_set.all().order_by("year"):
#                         row.append(
#                             f"year-{yearly_target_value.year.year}\n\n{yearly_target_value.target_value}"
#                         )
#                         if yearly_target_value.year.year <= current_year:
#                             try:
#                                 sub_row.insert(
#                                     sub_row_count, Paragraph(str(target.unit_of_measure.get_actual_data(indicator_obj)))
#                                 )
#                             except AttributeError:
#                                 sub_row.insert(
#                                     sub_row_count, Paragraph("")
#                                 )
#                         else:
#                             sub_row.insert(
#                                 sub_row_count, Paragraph("")
#                             )
#                         sub_row_count += 1

#                     data.append(row)
#                     data.append(sub_row)

#                     # This iter_count is used to create a tuple for styling the Baseline column(by how much the coumn
#                     # should span) in the table e.g ('SPAN', (0, 1), (0, 2))
#                     if iter_count == 0:
#                         third_column_sr += 1
#                         third_column_er = third_column_sr + 1
#                     else:
#                         third_column_sr += 2
#                         third_column_er = third_column_sr + 1
#                     iter_count += 1

#                     row_column_spans.append(
#                         (
#                             "SPAN",
#                             (third_column_sc, third_column_sr),
#                             (third_column_ec, third_column_er),
#                         )
#                     )

#                     actual_values_row_colorfills.append(
#                         (
#                             "BACKGROUND",
#                             (
#                                 actual_values_col_colorfill_start,
#                                 actual_values_row_colorfill_start,
#                             ),
#                             (
#                                 actual_values_col_colorfill_end,
#                                 actual_values_row_colorfill_end,
#                             ),
#                             colors.Color(
#                                 red=(216.0 / 255), green=(215.0 / 255), blue=(215 / 255)
#                             ),
#                         )
#                     )
#                     actual_values_row_colorfill_start += 2
#                     actual_values_row_colorfill_end += 2

#                     # Start over the iteration with empty list
#                     row = []
#                     # Start over the iteration with two empty rows
#                     sub_row = ["", ""]
#             else:
#                 continue

#         return (data, row_column_spans, actual_values_row_colorfills)


# def sub_project_form(training):
#     try:
#         from tralard.forms.sub_project import (
#             SubProjectForm,
#         )  # don't move this import on top
#     except:
#         pass
#     subproject_update_form = SubProjectForm(instance=training)
#     return subproject_update_form


# def save_to_temp_dir(base_dir, file_obj):
#     file_system_storage = FileSystemStorage()

#     path_name = f"{BASE_TEMP_DIR}{base_dir}"

#     if not os.path.exists(path_name):
#         os.makedirs(path_name)

#     clean_image_name = file_obj.name.lower().replace(' ', '_')

#     file_system_storage.save(f"{path_name}/{clean_image_name}", file_obj)

#     local_v = os.path.join(path_name, clean_image_name)

#     return local_v


# def delete_temp_dir(base_dir):
#     path_name = f"{BASE_TEMP_DIR}{base_dir}"
#     if os.path.exists(path_name):
#         shutil.rmtree(path_name)


# def delete_temp_file(file_obj):
#     clean_image_name = file_obj.name.lower().replace(' ', '_')
#     if os.path.exists(clean_image_name):
#         os.remove(clean_image_name)


# def sub_project_update_form(instance):
#     try:
#         from tralard.forms.sub_project import SubProjectForm  # don't move this import on top
#     except:
#         pass
#     subproject_update_form = SubProjectForm(instance=instance)
#     return subproject_update_form


# def sub_project_create_form():
#     try:
#         from tralard.forms.sub_project import SubProjectForm  # don't move this import on top
#     except:
#         pass
#     subproject_update_form = SubProjectForm()
#     return subproject_update_form


# def validate_photo_gps_range(max_magnitude, img_path, ward_location):
#     range_is_valid = False
#     distance = 0
#     # Verify that this is a valid image
#     try:
#         image_pil = Image.open(img_path)
#         image_pil.verify()
#     except IOError as e:
#         error_flag = f"[URL> {img_path}] This image could not be opened due to: {e}"
#         logger.error(error_flag)

#     with open(img_path, "r+b") as src_file:
#         image = ImageSource(src_file)
#         if image.has_exif:
#             # extract geographics
#             geotags = get_image_geotagging(image)
#             image_latitude = use_decimal_from_dms_util(geotags["GPSLatitude"], geotags["GPSLatitudeRef"])
#             image_longitude = use_decimal_from_dms_util(geotags['GPSLongitude'], geotags['GPSLongitudeRef'])
#             coordinates_obj = {
#                 "image_latitude": image_latitude,
#                 "image_longitude": image_longitude,
#                 "ward_latitude": float(ward_location.coords[0]),
#                 "ward_longitude": float(ward_location.coords[1]),
#             }
#             logger.info(f"Completed obtaining location points:\n {coordinates_obj}")
#             distance = use_haversine_util(coordinates_obj)
#             if distance > max_magnitude:
#                 validation_flag = f"Invalid Distance of {distance} km. Only images within {max_magnitude} kilometer " \
#                                   f"from ward location allowed."
#                 logger.warning(validation_flag)
#             else:
#                 range_is_valid = True
#     response = {
#         "range_is_valid": range_is_valid,
#         "distance": distance
#     }
#     return response


# def use_haversine_util(coordinates):
#     """
#         Calculate distance between ward location & image GPS with haversine trigonometric formulae

#         Parameters
#         ----------
#         coordinates : GPS coordinates for the image and ward location

#         Returns
#         -------
#         distance: (float): shortest distance between two points in kilometers.
#         i.e >>> '1.2324' kilometers

#     """
#     distance = 0  # initial distance
#     earth_radius = 6371  # mean radius

#     ward_latitude = float(coordinates["ward_latitude"])
#     image_latitude = float(coordinates["image_latitude"])
#     ward_longitude = float(coordinates["ward_longitude"])
#     image_longitude = float(coordinates["image_longitude"])
#     logger.error(f"Image Coords: ({image_latitude, image_longitude}) \n Ward Coords: ({ward_latitude, ward_longitude})")

#     # distance between latitudes and longitudes
#     latitude_magitude = (ward_latitude - image_latitude) * math.pi / 180.0
#     longitude_magitude = (ward_longitude - image_longitude) * math.pi / 180.0

#     # convert to radians to pass to the trig functions
#     image_latitude = image_latitude * math.pi / 180.0
#     ward_latitude = ward_latitude * math.pi / 180.0

#     # apply function of the sine and get the angle
#     angle = (
#             pow(math.sin(latitude_magitude / 2), 2) +
#             pow(math.sin(longitude_magitude / 2), 2) *
#             math.cos(image_latitude) *
#             math.cos(ward_latitude)
#     )
#     cosine_magnitude = 2 * math.asin(math.sqrt(angle))
#     distance = cosine_magnitude * earth_radius
#     logger.error(f"Calculated distance: {distance} kilometers")
#     return distance


# def use_decimal_from_dms_util(dms, ref):
#     """
#         Sexagesimal DMS value conversion system
#         Parameters
#         ----------
#         dms : Coords in Degrees, minutes and seconds
#         ref: Reference
#         Returns
#         -------
#         decimal_degrees: (float): GPS coordinates as decimals.
#         i.e >>> '((-15.440784222222222, 28.359679111111113))' kilometers
#     """
#     decimal_degrees = float(dms[0]) + float(dms[1]) / 60 + float(dms[2]) / 3600
#     if ref == "S" or ref == "W":
#         decimal_degrees = -decimal_degrees
#     return decimal_degrees


# def get_image_geotagging(exif):
#     """
#             Extract from image demographics the degrees, minutes, and seconds.
#             Parameters
#             ----------
#             exif : Image meta data
#             Returns
#             -------
#             geotagging: (dict): GPS coordinates for the image in DMS format.
#             i.e >>> '(Latitude: 15; 35; 16.43543858658), (Longitude: 28; 16; 29.324234200)'
#     """
#     # K^V labeled collection
#     geotagging = {
#         "GPSLatitude": exif.gps_latitude, "GPSLatitudeRef": exif.gps_latitude_ref,
#         "GPSLongitude": exif.gps_longitude, "GPSLongitudeRef": exif.gps_longitude_ref
#     }
#     return geotagging
