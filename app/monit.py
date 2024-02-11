import os, json, argparse, time, logging
from modules.Actions import getAllInfos, listReports, getLastReport, getAverage

with open("/etc/monit/config.json") as f:
    config = json.load(f)

logging.basicConfig(filename=os.path.join(config['log_dir'], f'monit-{time.strftime("%Y%m%d-%H%M")[0:12]}.log'),
					format='%(asctime)s %(message)s', 
					filemode='a',
                    level=logging.INFO) 

parser = argparse.ArgumentParser(description='Monit Tool | python3.11.2')

parser.add_argument('-c', '--check', action='store_true', help='Check system resources and record data')
parser.add_argument('-l','--list', action='store_true', help='List available reports')
parser.add_argument('-gL','--get_last', action='store_true', help='Get the last report')
parser.add_argument('-avg','--get_avg', type=int, metavar='X', help='Get average of the last X hours')

args = parser.parse_args()

async def main():

    if args.check:
        logging.info("| ⏲️ Checking resources and recording data")
        print(str(getAllInfos()))
        logging.info("| ✅ checked ")

    elif args.list:
        logging.info("| ⏲️ List command called from user")
        print("\n".join(str(reports) for reports in listReports()))
        logging.info('| ✅command succeed')

    elif args.get_last:
        logging.info('| ⏲️ Command get_last called from user')
        getLastReport()
        logging.info('| ✅command get_last succeed')

    elif args.get_avg is not None:
        logging.info('| ⏲️ Command get_avg called from user')
        last_x_hours = args.get_avg
        report = getAverage(last_x_hours)
        logging.info('| ✅command get-avg succeed')
        return f"""Average report for the last {last_x_hours} hours : \n
                cpu_percent : {str(report["cpu"])}% \n
                ram_percent : {str(report["ram"])}% \n
                disk_percent : {str(report["disk"])}%"""
        
    else:
        print('Unknown command. Use monit -h to see how to use the app.')

if __name__ == '__main__':

    import asyncio
    asyncio.run(main())