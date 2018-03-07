import asynctest

from juju.controller import Controller


class TestControllerConnect(asynctest.TestCase):
    @asynctest.patch('juju.client.connector.Connector.connect_controller')
    async def test_no_args(self, mock_connect_controller):
        c = Controller()
        await c.connect()
        mock_connect_controller.assert_called_once_with(None)

    @asynctest.patch('juju.client.connector.Connector.connect_controller')
    async def test_with_controller_name(self, mock_connect_controller):
        c = Controller()
        await c.connect(controller_name='foo')
        mock_connect_controller.assert_called_once_with('foo')

    @asynctest.patch('juju.client.connector.Connector.connect')
    async def test_with_endpoint_and_no_auth(self, mock_connect):
        c = Controller()
        with self.assertRaises(TypeError):
            await c.connect(endpoint='0.1.2.3:4566')
        self.assertEqual(mock_connect.call_count, 0)

    @asynctest.patch('juju.client.connector.Connector.connect')
    async def test_with_endpoint_and_userpass(self, mock_connect):
        c = Controller()
        with self.assertRaises(TypeError):
            await c.connect(endpoint='0.1.2.3:4566', username='dummy')
        await c.connect(endpoint='0.1.2.3:4566',
                        username='user',
                        password='pass')
        mock_connect.assert_called_once_with(endpoint='0.1.2.3:4566',
                                             username='user',
                                             password='pass')

    @asynctest.patch('juju.client.connector.Connector.connect')
    async def test_with_endpoint_and_bakery_client(self, mock_connect):
        c = Controller()
        await c.connect(endpoint='0.1.2.3:4566', bakery_client='bakery')
        mock_connect.assert_called_once_with(endpoint='0.1.2.3:4566',
                                             bakery_client='bakery')

    @asynctest.patch('juju.client.connector.Connector.connect')
    async def test_with_endpoint_and_macaroons(self, mock_connect):
        c = Controller()
        await c.connect(endpoint='0.1.2.3:4566',
                        macaroons=['macaroon'])
        mock_connect.assert_called_with(endpoint='0.1.2.3:4566',
                                        macaroons=['macaroon'])
        await c.connect(endpoint='0.1.2.3:4566',
                        bakery_client='bakery',
                        macaroons=['macaroon'])
        mock_connect.assert_called_with(endpoint='0.1.2.3:4566',
                                        bakery_client='bakery',
                                        macaroons=['macaroon'])

    @asynctest.patch('juju.client.connector.Connector.connect_controller')
    @asynctest.patch('juju.client.connector.Connector.connect')
    async def test_with_posargs(self, mock_connect, mock_connect_controller):
        c = Controller()
        await c.connect('foo')
        mock_connect_controller.assert_called_once_with('foo')
        with self.assertRaises(TypeError):
            await c.connect('endpoint', 'user')
        await c.connect('endpoint', 'user', 'pass')
        mock_connect.assert_called_once_with(endpoint='endpoint',
                                             username='user',
                                             password='pass')
        await c.connect('endpoint', 'user', 'pass', 'cacert', 'bakery',
                        'macaroons', 'loop', 'max_frame_size')
        mock_connect.assert_called_with(endpoint='endpoint',
                                        username='user',
                                        password='pass',
                                        cacert='cacert',
                                        bakery_client='bakery',
                                        macaroons='macaroons',
                                        loop='loop',
                                        max_frame_size='max_frame_size')
