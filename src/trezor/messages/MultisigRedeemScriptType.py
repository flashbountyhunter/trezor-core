# Automatically generated by pb2py
import protobuf as p
from .HDNodePathType import HDNodePathType


class MultisigRedeemScriptType(p.MessageType):
    FIELDS = {
        1: ('pubkeys', HDNodePathType, p.FLAG_REPEATED),
        2: ('signatures', p.BytesType, p.FLAG_REPEATED),
        3: ('m', p.UVarintType, 0),
    }

    def __init__(
        self,
        pubkeys: list = None,
        signatures: list = None,
        m: int = None,
        **kwargs,
    ):
        self.pubkeys = [] if pubkeys is None else pubkeys
        self.signatures = [] if signatures is None else signatures
        self.m = m
        p.MessageType.__init__(self, **kwargs)
