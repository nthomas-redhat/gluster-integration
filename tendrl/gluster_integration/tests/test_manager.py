from mock import MagicMock

from tendrl.gluster_integration import ini2json
from tendrl.gluster_integration.tests.test_gluster_integration import \
    TestGluster_integration


class Test_manager(TestGluster_integration):
    def Initialize(self, body):
        self.Manager.subprocess = self
        self.Manager.ini2json = self
        filename = self._makeFile('manager', body)
        self.sections = ini2json.ini_to_dict(filename)

    def test_manager_with_peer(self):
        body = """[Global]\nop-version:40000 \
        \n[Peers]\npeer1.uuid=1\npeer1.hostnames=pytest" \
        \nPeer1.primary_hostname=host1" \
        \npeer1.state=active"""
        self.Initialize(body)
        self.Manager.time.time = MagicMock(return_value=1477237162.990813)
        self.managerobj._discovery_thread._run()
        self.Manager.Peer.assert_called_with(
            cluster_id=self.clusterid,
            hostname='host1"', peer_uuid='1', state='active',
            updated='1477237162.99'
            )

    def test_manager_with_volume(self):
        body = """[Global]\nop-version:40000 \
        \n[Volumes]\nvolume1.id=1\nvolume1.type=abc" \
        \nvolume1.name=brick1\nvolume1.status=active\nvolume1.brickcount=1"""
        self.Initialize(body)
        self.managerobj._discovery_thread._run()
        self.Manager.Volume.assert_called_with(
            brick_count='1', cluster_id=self.clusterid,
            name='brick1', status='active',
            vol_id='1', vol_type='abc"'
            )

    def test_manager_with_brick(self):
        body = """[Global]\nop-version:40000 \
        \n[Volumes]\nvolume1.id=1\nvolume1.type=abc" \
        \nvolume1.name=brick1\nvolume1.status=active\nvolume1.brickcount=1 \
        \nvolume1.brick1.path=/tmp\nvolume1.brick1.hostname=abc \
        \nvolume1.brick1.port=80\nvolume1.brick1.status=active \
        \nvolume1.brick1.filesystem_type=FAT12 \
        \nvolume1.brick1.mount_options=abc"""
        self.Initialize(body)
        self.managerobj._discovery_thread._run()
        self.Manager.Brick.assert_called_with(
            cluster_id=self.clusterid,
            filesystem_type='FAT12', hostname='abc', mount_options='abc',
            path='/tmp', port='80', status='active', vol_id='1'
            )

    def test_manager_with_peer_keyerror(self):
        body = """[Global]\nop-version:40000\n[Peers]\npeer.uuid=1"""
        self.Initialize(body)
        self.managerobj._discovery_thread._run()
        assert not self.Manager.Peer.called

    def test_manager_with_volume_keyerror(self):
        body = """[Global]\nop-version:40000\n[Volumes]\n"""
        self.Initialize(body)
        self.managerobj._discovery_thread._run()
        assert not self.Manager.Volume.called

    def test_manager_with_brick_keyerror(self):
        body = """[Global]\nop-version:40000\n \
        [Volumes]\nvolume1.id=1\nvolume1.type=abc" \
        \nvolume1.name=brick1\nvolume1.status=active\nvolume1.brickcount=1"""
        self.Initialize(body)
        self.managerobj._discovery_thread._run()
        assert not self.Manager.Brick.called

    def test_main(self):
        self.Manager.gevent = MagicMock()
        self.Manager.main()
        self.Manager.gevent.signal.assert_called()

    """Mocked subprocess call to stop while loop"""
    def call(self, *args):
        self.managerobj._discovery_thread.stop()

    """Mocked ini2json for return temp file"""
    def ini_to_dict(self, *args):
        return self.sections
