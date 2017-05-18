from lback.utils import lback_output

def make_connection_string( agent_object ):
     connection_string = "{}:{}".format(agent_object.host, agent_object.port)
     return connection_string

def safe_rpc( agent, agent_fn ):
    res = None
    try:
        res = agent_fn ( agent[ 1 ] )
    except Exception,ex:
        lback_output( ex )
        lback_output("Unable to send command to LBACK AGENT: {}".format( make_connection_string( agent[ 0 ] )))
    return res

