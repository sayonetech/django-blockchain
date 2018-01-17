from django.conf.urls import url
from chain.api.v0.views import BlockApiView, ChainApiView, LatestBlockApiView, BlockCreateView, PeerApiView, TransactionsList

urlpatterns = [
    url(r'^blocks/(?P<chain_name>[A-Za-z0-9-]+)/latest$', LatestBlockApiView.as_view(), name='latest-block'),
    url(r'^blocks/(?P<chain_name>[A-Za-z0-9-]+)/mine-block$', BlockCreateView.as_view(), name='mine-block'),
    url(r'^blocks/(?P<hash>[A-Za-z0-9-]+)$', BlockApiView.as_view(), name='get'),
    url(r'^chains/(?P<name>[A-Za-z0-9-]+)$', ChainApiView.as_view(), name='chain'),
    url(r'^peers/$', PeerApiView.as_view(), name='peers'),
    url(r'^peers/add$', PeerApiView.as_view(), name='add-peer'),
    url(r'^transaction/$', TransactionsList.as_view(), name='transaction'),
]
