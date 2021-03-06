import etcd

from tendrl.commons import objects
from tendrl.commons.utils import log_utils as logger


class VolumeStarted(objects.BaseAtom):
    def __init__(self, *args, **kwargs):
        super(VolumeStarted, self).__init__(*args, **kwargs)

    def run(self):
        logger.log(
            "info",
            NS.publisher_id,
            {"message": "Checking if volume %s started" %
             self.parameters['Volume.volname']},
            job_id=self.parameters["job_id"],
            flow_id=self.parameters["flow_id"],
            integration_id=NS.tendrl_context.integration_id
        )
        try:
            fetched_volume = NS.gluster.objects.Volume(
                vol_id=self.parameters['Volume.vol_id']
            ).load()
        except etcd.EtcdKeyNotFound:
            logger.log(
                "error",
                NS.publisher_id,
                {"message": "Volume %s does not exist" %
                 self.parameters['Volume.volname']},
                job_id=self.parameters["job_id"],
                flow_id=self.parameters["flow_id"],
                integration_id=NS.tendrl_context.integration_id
            )
            return False

        if fetched_volume.status == "Started":
            logger.log(
                "info",
                NS.publisher_id,
                {"message": "Volume %s is started" %
                 self.parameters['Volume.volname']},
                job_id=self.parameters["job_id"],
                flow_id=self.parameters["flow_id"],
                integration_id=NS.tendrl_context.integration_id
            )
            return True
        else:
            logger.log(
                "warning",
                NS.publisher_id,
                {"message": "Volume %s is already stopped" %
                 self.parameters['Volume.volname']},
                job_id=self.parameters["job_id"],
                flow_id=self.parameters["flow_id"],
                integration_id=NS.tendrl_context.integration_id
            )
            return False
