import hidmsr.commands as cmds
import hidmsr.convert as conv
import parse
import csv
from datetime import datetime
import time

def main():
    m = cmds.MSRDevice()
    m.set_hico()
    m.set_bpi(210, 75, 210)

    filename = f"{datetime.now().strftime('%Y-%m-%d')}.csv"

    with open(filename, 'a', newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(['Timestamp', 'ID'])
        
        print(f"Ready to read cards. Writing to {filename}. Press Ctrl+C to exit.")
        try:
            while True:
                out = m.read()
                data = conv.decode_msr_data(out)
                card_id = parse.extract_id(data)
                
                if card_id:
                    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                    writer.writerow([timestamp, card_id])
                    print(f"Recorded ID: {card_id} at {timestamp}")
                    csvfile.flush()
                time.sleep(0.1)  # Small delay to prevent CPU overuse
                
        except KeyboardInterrupt:
            print("\nStopping card reader...")
        except Exception as e:
            print(f"\nError occurred: {str(e)}")
        finally:
            print("Program terminated.")

if __name__ == "__main__":
    main()
