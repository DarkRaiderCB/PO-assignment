from together import Together
from parser import *
from dotenv import load_dotenv
import os

load_dotenv()

client = Together(api_key=os.getenv("API_KEY"))

def classify_email(subject, body, attachment_paths=[]):
    """
    Use Llama API from Together for enhanced email classification.
    """
    sys_prompt = f"""
    Examples:
1. Subject: Purchase Order - PO# 87432
   Body: Dear GreenSupply Inc., Please find attached Purchase Order number 87432 for the following items: 
   - Item: Office Desks 
     Quantity: 25 
     Unit Price: $120.00 
     Total Price: $3,000.00 
   Please confirm receipt of this order and provide an estimated delivery date.
   Classification: purchase order email

2. Subject: Information Request for Career Opportunities
   Body: Dear HR, I came across your job openings page. Could you provide more details about the role of Senior Software Engineer? Thanks.
   Classification: non-purchase order email

3. Subject: PO Change Request - Item Modification
   Body: Dear EcoSource, Modify PO# to include eco-safe dyes. Sincerely, Rachel EcoArt
   Classification: purchase order email

4. Subject: Invoice #HOTEL-2024-002: Stay at Hotel Luxe
   Body: Thank you for staying at Hotel Luxe. Attached is your invoice #HOTEL-2024-002 for INR 6,800. We hope to see you again!
   Classification: non-purchase order email

5. Subject: Need Supplies ASAP - PO# 99765
   Body: URGENT Dear SpeedySupply Co., We urgently require the following items: 
   - Item: Power Adapters 
     Quantity: 50 
     Unit Price: $35.00 
     Total: $1,750.00 
   Please ensure delivery by December 6th, 2024. Let us know if you can meet this deadline.
   Classification: purchase order email

6. Subject: Payment Confirmation for Invoice #INV-54321
   Body: We have received your payment of INR 2,000 for Invoice #INV-54321. Thank you for your prompt payment.
   Classification: non-purchase order email

7. Subject: Subscription Order - Monthly IT Supplies
   Body: Dear SupplyNet, Please set up a subscription for the following items: 
   - Item: Printer Ink, Office Paper 
     Frequency: Monthly 
     Total: $500.00 per month 
   Ensure delivery on the 1st of each month. Sincerely, Neil Harris
   Classification: purchase order email

8. Subject: Request for Price List: Building Materials
   Body: Dear Supplier, could you share your latest price list for building materials, including cement and steel? Also, mention bulk discounts if any.
   Classification: non-purchase order email

9. Subject: Rush Order Needed - Replacement Screens
   Body: Dear RepairWorks Inc., Please expedite the following order: 
   - Item: Replacement Screens 
     Quantity: 100 
     Unit Price: $25.00 
     Total: $2,500.00 
   We need delivery by December 5th, 2024. Thank you for your immediate attention.
   Classification: purchase order email

10. Subject: Proforma Invoice #P-INV-0045 for Your Reference
    Body: Attached is the proforma invoice #P-INV-0045 for your recent quotation request. Total: INR 3,600. This is not a payment request.
    Classification: non-purchase order email

11. Subject: Bulk Order Inquiry for Stationery Supplies
    Body: Hello, I am interested in placing a bulk order for office stationery supplies. Please share your catalog and any available discounts for bulk purchases.
    Classification: non-purchase order email

12. Subject: International PO - Customs Documentation Required
    Body: Dear GlobalX Inc., Please ensure customs compliance for: 
    - Item: Solar Panels 
      Total: $15,000.00 
    Sincerely, Zara Green
    Classification: purchase order email

13. Subject: Refund Issued for Invoice #REF-99999
    Body: We have processed a refund of INR 1,500 for Invoice #REF-99999. The amount will reflect in your account within 5-7 working days.
    Classification: non-purchase order email

14. Subject: Invoice Overdue: Immediate Action Required
    Body: Your payment for Invoice #INV-87654 of INR 4,500 is overdue. Kindly settle it immediately to avoid service disruption.
    Classification: non-purchase order email

15. Subject: Service Order - IT Consultancy
    Body: Dear TechConsult Experts, Please provide the following services: 
    - Service: IT Infrastructure Audit 
      Hours: 30 
      Hourly Rate: $150.00 
      Total: $4,500.00 
    We expect a detailed report by December 15th, 2024. Regards, Tina Wong
    Classification: purchase order email

16. Subject: Limited Offer: Free Gift with Every Purchase
    Body: Shop now and receive a free gift with every purchase above $50. Don’t miss out on this exclusive deal! Visit www.spamstore.com.
    Classification: non-purchase order email

17. Subject: Customized Order - Branded Tote Bags
    Body: Dear LogoCraft Ltd., Please provide a quote for the following customized order: 
    - Item: Tote Bags with Company Logo 
      Quantity: 1,000 
      Customization: Full-color logo print 
    Include a detailed breakdown of material and labor costs. Best regards, Amelia Stone
    Classification: purchase order email

18. Subject: Final Reminder: Invoice #INV-13579 Due Soon
    Body: This is your final reminder that Invoice #INV-13579 of INR 3,250 is due on 2024-12-06. Please ensure payment by the due date.
    Classification: non-purchase order email

19. Subject: Inquiry About Training Program Availability
    Body: Dear Support, I would like to know the next available dates for your Data Science Training Program. Could you also share the registration process? Thanks.
    Classification: non-purchase order email

20. Subject: Bolts Requirement for Feb'24, Mar'24 & Apr'24

Body: Dear Sir/Madam,

Please find below the requirements for the month of Feb-2024. Kindly plan your actions accordingly and confirm acknowledgment along with raw material availability for M1 and M9 quantities.

CAT No.	M9 (Feb)	M2 (Mar)	M3 (Apr)	Receipt till 10.02.2024	Balance to Dispatch	Dispatch Required On
BT12456	55000	52000	53000	0	55000	12th Feb
BT14832	48000	50000	50000	0	48000	15th Feb
XL04567	45000	47000	47000	0	45000	18th Feb
CL60312	3000	4000	3000	1500	1500	20th Feb
CL60277	6000	8000	7000	2500	3500	20th Feb
CL60219	4000	4500	4000	1000	3000	20th Feb
CL60218	7000	0	6000	0	7000	20th Feb
CL60241	8000	9000	8500	4000	4000	20th Feb
XS01312	11000	10000	10500	0	11000	22nd Feb
Kindly expedite as per the schedule.

Best regards,

Classification: puchase order email

21. Subject: International Shipment PO# INT-65748
    Body: Dear Global Goods Ltd., Please find attached Purchase Order number INT-65748 for the following international shipment: 
    - Item: Organic Coffee Beans 
      Quantity: 2,000 lbs 
      Unit Price: $8.00/lb 
      Total Price: $16,000.00 
    Ensure all customs documentation is in order. Sincerely, Lila Monroe
    Classification: purchase order email

22. Subject: "Need specifications for components A102/B405/C3678",  
    Body: "Dear Team, Kindly share the detailed specifications for the components listed below. It would also be helpful if you could provide drawings or diagrams where applicable.  
      ItemNo Commodity Description  
      A102 Electrical CONNECTOR, 3-PIN  
      B405 Mechanical HEX BOLT M12 X 1.5  
      C3678 Electrical WIRING HARNESS, 5-METER"  
    Classification: non-purchase order email

    Based on above content, classify emails as purchase order or non-purchase orders. 
    Remember: 
    1. Enquiry, request for quotation, invoice emails, emails requesting specifications like size, price, etc., delivery confirmation, complaints, missing items etc. are NOT purchase orders.
    2. Emails suggesting dispatch, due amount/amount to be dispatched, balance amount to dispatch, preorders, payment date, etc are purchase orders.
    If the email is non-purchase order, further classify it as enquiry, invoice, bank notification, spam,etc. based on its content (mention both things explicilty, non-purchase order and the other category).
    JUST RESPOND THE EMAIL TYPE AND NOTHING ELSE. 
    """
    attachment_content = ""
    for attachment in attachment_paths:
      if attachment.endswith(('.pdf', '.xlsx', '.docx', '.jpeg', '.csv')):
          attachment_content = extract_attachment(attachment)
    response = client.chat.completions.create(
        model="meta-llama/Meta-Llama-3.1-8B-Instruct-Turbo",
        messages=[{"role": "system", "content": sys_prompt}, {"role":"user", "content": f"Subject:{subject}\nBody:{body}\nAttachments:{attachment_content}"}],
        max_tokens=1500,
        temperature=0,
        stream=True,
    )
    result = ""
    for token in response:
        if hasattr(token, "choices"):
            delta_content = token.choices[0].delta.content
            result += delta_content
    return result