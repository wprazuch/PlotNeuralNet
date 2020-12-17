
import sys
sys.path.append('../')
from pycore.tikzeng import *
from pycore.blocks  import *

arch = [ 
    to_head('..'), 
    to_cor(),
    to_begin(),
    
    #input
    to_input( '../examples/xray_circa.jpg' ),

    to_ConvConvRelu( name='ccr_b1', offset="(0,0,0)", to="(0,0,0)", width=(2,2), height=40, depth=40  ),
    to_Pool(name="pool_b1", offset="(0,0,0)", to="(ccr_b1-east)", width=1, height=32, depth=32, opacity=0.5),

    #block-001
    *block_2ConvPool( name='b2', botton='pool_b1', top='pool_b2', s_filer='', n_filer='', offset="(1,0,0)", size=(32,32,3.5), opacity=0.5 ),
    *block_2ConvPool( name='b3', botton='pool_b2', top='pool_b3', s_filer='', n_filer='', offset="(1,0,0)", size=(25,25,4.5), opacity=0.5 ),
    *block_2ConvPool( name='b4', botton='pool_b3', top='pool_b4', s_filer='',  n_filer='', offset="(1,0,0)", size=(16,16,5.5), opacity=0.5 ),

    #Bottleneck
    #block-005
    to_ConvConvRelu( name='ccr_b5', n_filer=('',''), offset="(2,0,0)", to="(pool_b4-east)", width=(8,8), height=8, depth=8, caption=""  ),
    to_connection( "pool_b4", "ccr_b5"),

    #Decoder
    *block_Unconv( name="b6", botton="ccr_b5", top='end_b6', s_filer='',  n_filer='', offset="(2.1,0,0)", size=(16,16,5.0), opacity=0.5 ),
    to_skip( of='ccr_b4', to='ccr_res_b6', pos=1.25),    
    *block_Unconv( name="b7", botton="end_b6", top='end_b7', s_filer='', n_filer='', offset="(2.1,0,0)", size=(25,25,4.5), opacity=0.5 ),
    to_skip( of='ccr_b3', to='ccr_res_b7', pos=1.25),    
    *block_Unconv( name="b8", botton="end_b7", top='end_b8', s_filer='', n_filer='', offset="(2.1,0,0)", size=(32,32,3.5), opacity=0.5 ),
    to_skip( of='ccr_b2', to='ccr_res_b8', pos=1.25),    
    
    *block_Unconv( name="b9", botton="end_b8", top='end_b9', s_filer='', n_filer='',  offset="(2.1,0,0)", size=(40,40,2.5), opacity=0.5 ),
    to_skip( of='ccr_b1', to='ccr_res_b9', pos=1.25),
    
    to_ConvSoftMax( name="soft1", s_filer='', offset="(0.75,0,0)", to="(end_b9-east)", width=1, height=40, depth=40, caption="" ),
    to_connection( "end_b9", "soft1"),
    to_output(pathfile='../examples/mask_circa.png', offset="(0,0,0)", to="(soft1-east)"),
    to_end() 
    ]


def main():
    namefile = str(sys.argv[0]).split('.')[0]
    to_generate(arch, namefile + '.tex' )

if __name__ == '__main__':
    main()
    
