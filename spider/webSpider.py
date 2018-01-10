import re  
from bs4 import BeautifulSoup  
  
email_id_example = """<br/> 
<div>The below HTML has the information that has email ids.</div>  
abc@example.com 
<div>xyz@example.com</div> 
<span>foo@example.com</span> 
"""  
  
soup = BeautifulSoup(email_id_example, "lxml")  
emailid_regexp = re.compile("\w[-\w.+]*@([A-Za-z0-9][-A-Za-z0-9]+\.)+[A-Za-z]{2,14}")  
first_email_id = soup.find(text=emailid_regexp)  
print(first_email_id)  
next_email_id = soup.find_next(text=emailid_regexp)  
print(next_email_id)  