from rest_framework import serializers
from chain.models import Block, Chain, Peer, Transactions

import logging

log = logging.getLogger(__name__)

class TransactionSerializer(serializers.ModelSerializer):

    class Meta:
        model = Transactions
        fields = ('sender', 'receiver', 'amount',)


class BlockSerializer(serializers.ModelSerializer):

    class Meta:
        model = Block
        fields = ('hash', 'previous_hash', 'data', 'time_stamp', 'index', 'nonce',)

    def as_json(self):
        self.is_valid()
        data = dict(self.validated_data)
        data['time_stamp'] = str(data['time_stamp'])
        return data


class ChainSerializer(serializers.ModelSerializer):
    block_set = BlockSerializer(many=True,
                                read_only=True,
                                allow_null=True)

    class Meta:
        model = Chain
        fields = ('name', 'block_set')


class PeerSerializer(serializers.ModelSerializer):

    class Meta:
        model = Peer
        fields = ('name', 'address',)