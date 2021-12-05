import sched, time

list = []

s = sched.scheduler(time.time, time.sleep)

sched_list = list()

def printn(text):
    print('This is...', text)

def schedule(time, name):
    s.enter(time, 1, printn, argument=(name,))


schedule(5,'Second')
schedule(3, 'First')


def schedule_covid_updates(update_name, update_interval):
    sched_list.append(update_name, update_interval)


s.run()