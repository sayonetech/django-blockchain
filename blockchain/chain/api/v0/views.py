# from snippets.models import Snippet
from rest_framework.permissions import AllowAny
from rest_framework import generics
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.renderers import TemplateHTMLRenderer
from chain.api.v0.serializers import BlockSerializer, ChainSerializer, PeerSerializer, TransactionSerializer
from chain.models import *


class BlockApiView(generics.RetrieveAPIView):
    permission_classes = (AllowAny,)
    serializer_class = BlockSerializer
    queryset = Block.objects.all()
    lookup_field = 'hash'


class BlockCreateView(generics.CreateAPIView):
    permission_classes = (AllowAny,)
    serializer_class = BlockSerializer

    def create(self, request, *args, **kwargs):
        serializer = BlockSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        block = Block(**serializer.validated_data)
        block.chain, _ = Chain.objects.get_or_create(name=kwargs.get('chain_name'))
        print(block.is_valid_block(block.chain.last_block))
        print("# ", request.data)


        if not block.chain.is_valid_next_block(block):
            return Response({}, status=status.HTTP_304_NOT_MODIFIED)
        try:
            block.save()
        except Exception as e:
            print(" ON SAVE ::", e)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)


class LatestBlockApiView(generics.GenericAPIView):
    permission_classes = (AllowAny,)
    serializer_class = BlockSerializer

    def get(self, request, *args, **kwargs):
        instance = Block.objects\
            .filter(chain__name=kwargs.get('chain_name'))\
            .order_by('index')\
            .last()
        return Response(BlockSerializer(instance).data,
                        status=status.HTTP_200_OK)


class ChainApiView(generics.RetrieveAPIView):
    permission_classes = (AllowAny,)
    serializer_class = ChainSerializer
    queryset = Chain.objects.all()
    lookup_field = 'name'


class PeerApiView(generics.ListAPIView,
                  generics.CreateAPIView):
    permission_classes = (AllowAny,)
    serializer_class = PeerSerializer
    queryset = Peer.objects.all()


class TransactionsList(APIView):
    """
    Create a new transaction.
    """
    renderer_classes = [TemplateHTMLRenderer]
    template_name = 'transaction.html'

    def get(self, request, *args, **kwargs):
        serializer = TransactionSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            transaction = Transactions(**serializer.validated_data)
            transaction.save()
            if Transactions.objects.filter(added_to_block = False).count() >= 2:
                trans = Transactions.objects.filter(added_to_block = False)
                t = []
                for item in trans:
                    data1 = item.__dict__
                    data1.pop("_state",0)
                    data1.pop("added_to_block",0)
                    t.append(data1)
                trans.update(added_to_block=True)
                block_obj = Block.mine_block("first",t,)
                block_obj.save()
                headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)