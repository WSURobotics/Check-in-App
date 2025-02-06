import hidmsr.commands as cmds
import hidmsr.convert as conv
import utils
import csv
from datetime import datetime
import time
import os
from discord_webhook import DiscordWebhook

def count_id_occurrences(filename, target_id):
    count = 0
    try:
        with open(filename, 'r') as csvfile:
            reader = csv.reader(csvfile)
            next(reader)  # Skip header
            for row in reader:
                if len(row) >= 3 and row[2] == target_id:
                    count += 1
    except Exception as e:
        print(f"Error reading file: {str(e)}")
        return 0
    return count

def main():
    data_dir = "Data"
    logs_dir = os.path.join(data_dir, "Logs")
    os.makedirs(logs_dir, exist_ok=True)

    m = cmds.MSRDevice()
    m.set_hico()
    m.set_bpi(210, 75, 210)

    #filename = os.path.join(logs_dir, f"{datetime.now().strftime('%m-%d-%y')}.csv")
    filename = os.path.join(logs_dir, "open_hours_log.csv")
    file_exists = os.path.exists(filename) and os.path.getsize(filename) > 0

    with open(filename, 'a', newline='') as csvfile:
        writer = csv.writer(csvfile)
        if not file_exists:
            writer.writerow(['Date', 'Time', 'ID', 'Status'])
        
        webhook_url = "https://discord.com/api/webhooks/1337131683861758054/XMlMEcrbmBfBeTdXDgEEFOxfMZq5OJQXbd7dtAuUBhvo1GODsWNutASDqydWOjsLuxvx"
        webhook_in = DiscordWebhook(url=webhook_url, content="The club room is open")
        webhook_out = DiscordWebhook(url=webhook_url, content="The club room is closed")

        print(f"Ready to read cards. Writing to {filename}. Press Ctrl+C to exit.")
        last_card_id = None
        last_read_time = 0
        CARD_COOLDOWN = 1 
        
        try:
            while True:
                out = m.read()
                data = conv.decode_msr_data(out)
                card_id = utils.extract_id(data)
                current_time = time.time()
                
                if card_id:
                    # Clear last_card_id if enough time has passed
                    if current_time - last_read_time > CARD_COOLDOWN:
                        last_card_id = None
                    
                    if card_id != last_card_id:
                        current_date = datetime.now().strftime('%Y-%m-%d')
                        current_time_str = datetime.now().strftime('%H:%M:%S')
                        
                        try:
                            count = count_id_occurrences(filename, card_id)
                            if count % 2 == 1:
                                status = "Out"
                                webhook_out.execute()
                            else:
                                status = "In"
                                webhook_in.execute()
                            
                            writer.writerow([current_date, current_time_str, card_id, status])
                            print(f"Recorded ID: {card_id} at {current_date}, {current_time_str} - {status}")
                            csvfile.flush()


                            last_card_id = card_id
                            last_read_time = current_time
                        except Exception as e:
                            print(f"Error processing card: {str(e)}")
                
                time.sleep(0.1)
                
        except KeyboardInterrupt:
            print("\nStopping card reader...")
        except Exception as e:
            print(f"\nError occurred: {str(e)}")
        finally:
            print("Program terminated.")
if __name__ == "__main__":
    main()