import os
import optparse


def launch_args():
    '''Process the arguments given by the user. Catch any possible errors.'''

    # Default networks allowed
    networks = ['ropsten', 'mainnet', 'kovan', 'rinkeby']

    # Define the options
    parser = optparse.OptionParser()
    parser.add_option('-s', '--source', 
        dest='source',
        help=('Target contract to compile and launch. Only use the name of the '
            'contract. For example, a smart contract written in the file named'
            ' (Greeter.sol), just input (Greeter)')
    )
    parser.add_option('-n', '--network',
        dest='network',
        help= ('The target network to launch to. Options are: mainnet, ropsten,' 
        ' rinkeby, and kovan')
    )
    parser.add_option('-c', '--compile-only',
        dest='compile_only',
        help= ('Choose whether to compile the contract and exit before'
        ' launching it to the network. Leave out this argument if you want to '
        'launch this contract, as the default is False.')
    )

    (opts, args) = parser.parse_args()

    if args:
        # Do not accept options without their tag
        raise Exception('Each option must be manually determined using the prop'
            +'er options. try \n\n>>>python launch.py --help\n\nto see proper'
            +' arguments'
         )

    # Source must be included and it must actually exist
    assert opts.source is not None, 'Contract source required.'
    assert opts.source in os.listdir('Contracts/'), 'Contract directory not found.'
    assert opts.source+'.sol' in os.listdir('Contracts/'+opts.source+'/'), 'Contract source not found.'

    if opts.network is None:
        print('No network given. Using ropsten by default')
        opts.network = 'ropsten'
    else:
        assert opts.network in networks, 'Not a valid choice of network.'

    if opts.compile_only is None:
        opts.compile_only = False
    else:
        print(
            'compile_only interpreted as True. Will not launch contract to network.'
        )
        opts.compile_only = True

    return (opts.source, opts.network, opts.compile_only)



def interact_args():
    '''Process the arguments given by the user. Catch any possible errors.'''

    # Default networks allowed
    networks = ['ropsten', 'mainnet', 'kovan', 'rinkeby']

    # Define the options
    parser = optparse.OptionParser()
    parser.add_option('-s', '--source', 
        dest='source',
        help=('Target contract to compile and launch. Only use the name of the '
            'contract. For example, a smart contract written in the file named'
            ' (Greeter.sol), just input (Greeter)')
    )
    parser.add_option('-n', '--network',
        dest='network',
        help= ('The target network to launch to. Options are: mainnet, ropsten,' 
        ' rinkeby, and kovan')
    )

    (opts, args) = parser.parse_args()

    if args:
        # Do not accept options without their tag
        raise Exception('Each option must be manually determined using the prop'
            +'er options. try \n\n>>>python launch.py --help\n\nto see proper'
            +' arguments'
         )

    # Source must be included and it must actually exist
    assert opts.source is not None, 'Contract source required.'
    assert opts.source in os.listdir('Contracts/'), 'Contract directory not found.'
    assert opts.source+'.sol' in os.listdir('Contracts/'+opts.source+'/'), 'Contract source not found.'

    if opts.network is None:
        print('No network given. Using ropsten by default')
        opts.network = 'ropsten'
    else:
        assert opts.network in networks, 'Not a valid choice of network.'

    return (opts.source, opts.network)