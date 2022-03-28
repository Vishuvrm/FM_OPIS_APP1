import win32com.client as client
import time
import pywintypes

def wait_for_task(name, refresh, logger):
    while True:
        try:
            scheduler = client.Dispatch("Schedule.Service")
            scheduler.Connect()

            tasks = scheduler.GetRunningTasks(1)
            names = [tasks.Item(i + 1).Name for i in range(tasks.Count)]
            if name in names:
                time.sleep(refresh)
                continue
            else:
                time.sleep(refresh+1)
                return False
        except pywintypes.com_error:
            logger.exception(f"\n\nReconnecting to {name}...\n")

        except Exception as e:
            logger.exception(e)

if __name__ == "__main__":
    wait_for_task("testing", 1)
