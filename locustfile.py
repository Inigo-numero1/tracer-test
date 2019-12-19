import locust

class TranslateTaskSet(locust.TaskSet):

    @locust.task
    def translate(self):
        return self.client.get('/index')


class TranslateUser(locust.HttpLocust):
    task_set = TranslateTaskSet
    min_wait = 800
    max_wait = 1000
