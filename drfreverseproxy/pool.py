from urllib3.poolmanager import PoolManager as PoolManager_, SSL_KEYWORDS

from .connection import HTTPConnectionPool, HTTPSConnectionPool


pool_classes_by_scheme = {
    'http': HTTPConnectionPool,
    'https': HTTPSConnectionPool,
}


class PoolManager(PoolManager_):
    def _new_pool(self, scheme, host, port, request_context=None):
        """
        Create a new :class:`ConnectionPool` based on host, port and scheme.
        This method is used to actually create the connection pools handed out
        by :meth:`connection_from_url` and companion methods. It is intended
        to be overridden for customization.

        If ``request_context`` is provided, it is provided as keyword arguments
        to the pool class used. This method is used to actually create the
        connection pools handed out by :meth:`connection_from_url` and
        companion methods. It is intended to be overridden for customization.
        """

        pool_cls = pool_classes_by_scheme[scheme]
        if request_context is None:
            request_context = self.connection_pool_kw.copy()

        # Although the context has everything necessary to create the pool,
        # this function has historically only used the scheme, host, and port
        # in the positional args. When an API change is acceptable these can
        # be removed.
        for key in ('scheme', 'host', 'port'):
            request_context.pop(key, None)

        if scheme == 'http':
            for kw in SSL_KEYWORDS:
                request_context.pop(kw, None)

        return pool_cls(host, port, **request_context)
