Request:

curl -i -H "Content-Type: application/json"  -d 
'{"text": "The Trump team began its opening arguments in the Senate trial on Saturday, as Trump’s lawyers tried to sow doubt about the Democrats’ evidence that 
Trump asked Ukrainian leaders to investigative his political rival. The trial could conclude this week, depending on the mindset and demands of a handful of
moderate Republican senators with whom the president’s immediate fate now rests. If they vote with Democrats to call witnesses, then the trial could easily 
last an additional week and would buttress both the president’s State of the Union address as well as the Iowa caucuses.\\n\\nWhite House aides had been hoping 
to use the State of the Union address to lay out Trump’s agenda for the rest of the year as well as a potential second term, and lately Trump has tried to cast 
impeachment and the investigations into his conduct as one of his many accomplishments for the country."}'
 -X POST http://0.0.0.0:5000/api/v1/summarization/

Response 

[
  [
    "the trial could conclude this week , depending on the mindset and demands of a handful of moderate republican senators with whom the president 's immediate 
    fate now rests. if they vote with democrats to call witnesses , the trial would easily easily easily last an additional week. trump has tried to cast 
    impeachment and the investigations into his conduct as one of his many accomplishments for the country"
  ]
]
