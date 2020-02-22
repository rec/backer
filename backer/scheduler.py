import schedule as _schedule


def schedule(every, at, func):
    if '@' in every:
        if at:
            raise ValueError('Cannot use @ and at: at the same time')
        every, at = every.split('@')

    scheduler = getattr(_schedule.every(), every)
    if at:
        # Rewrite 4:32 to 04:32
        if len(at.split(':')[0]) < 2:
            scheduler = scheduler.at('0' + at)

    return scheduler.at(at).do(func)
