# Check-in-App
A Python program that tracks open hours and attendance using the hidmsr library and the MSR605X card reader

Open hours:
- Every club officer swipes into a room when they enter and swipes out when they leave
- When any officer is in the room, the room is marked as open
- When all officers are out, the room is marked as closed
- Officer ID's are put in the "officer_list" spreadsheet
- Room status log can be seen in the "open_hours_log" spreadsheet

Member attendance:
- When non-officers swipe their card, their ID is appended to a list
- You can count the number of times any ID appears up to see how many events they have attended
- Logs can be seen in the "member_attendance" spreadsheet