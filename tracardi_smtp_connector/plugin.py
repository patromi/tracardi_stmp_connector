from tracardi_plugin_sdk.domain.register import Plugin, Spec, MetaData
from tracardi_plugin_sdk.action_runner import ActionRunner
from tracardi_plugin_sdk.domain.result import Result
from tracardi_smtp_connector.model.smtp import Configuration
from tracardi_smtp_connector.service.sendman import PostMan


class SmtpDispatcherAction(ActionRunner):
    def __init__(self, **kwargs):
        self.config = Configuration(**kwargs)
        self.post = PostMan(self.config.server)

    async def run(self, payload):
        try:
            self.post.send(self.config.message)
            return Result(port='payload', value=True)
        except Exception as e:
            self.console.warning(repr(e))
            return Result(port='payload', value=False)


def register() -> Plugin:
    return Plugin(
        start=False,
        spec=Spec(
            module='tracardi_smtp_connector.plugin',
            className='SmtpDispatcherAction',
            inputs=["payload"],
            outputs=['payload'],
            init={
                'server': {
                    'smtp': "smtp.gmail.com",
                    'port': 587,
                    'username': None,
                    'password': None,
                    'timeout': 15
                },
                'message': {
                    "send_to": None,
                    "send_from": None,
                    "reply_to": None,
                    "title": None,
                    "message": None
                }
            },
            version='0.1',
            license="MIT",
            author="iLLu"

        ),
        metadata=MetaData(
            name='Send mail',
            desc='Send mail via defined smtp server.',
            type='flowNode',
            width=200,
            height=100,
            icon='email',
            group=["Connectors"]
        )
    )