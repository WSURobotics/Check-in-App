import hidmsr.commands as cmds
import hidmsr.convert as conv
import parse
import csv
from datetime import datetime
import time
import os

def main():
    m = cmds.MSRDevice()
    m.set_hico()
    m.set_bpi(210, 75, 210)

    filename = f"{datetime.now().strftime('%Y-%m-%d')}.csv"
    
    # Check if file exists and is not empty
    file_exists = os.path.exists(filename) and os.path.getsize(filename) > 0

    with open(filename, 'a', newline='') as csvfile:
        writer = csv.writer(csvfile)
        if not file_exists:
            writer.writerow(['Date', 'Time', 'ID'])
        
        print(f"Ready to read cards. Writing to {filename}. Press Ctrl+C to exit.")
        try:
            while True:
                out = m.read()
                data = conv.decode_msr_data(out)
                card_id = parse.extract_id(data)
                
                if card_id:
                    current_date = datetime.now().strftime('%Y-%m-%d')
                    current_time = datetime.now().strftime('%H:%M:%S')
                    writer.writerow([current_date, current_time, card_id])
                    print(f"Recorded ID: {card_id} at {current_date}, {current_time}")
                    csvfile.flush()
                time.sleep(0.1)
                
        except KeyboardInterrupt:
            print("\nStopping card reader...")
            
        except Exception as e:
            print(f"\nError occurred: {str(e)}")
        finally:
            print("Program terminated.")

if __name__ == "__main__":
    main()