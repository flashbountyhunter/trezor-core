from trezor import wire, ui


async def layout_get_address(ctx, msg):
    from trezor.messages.Address import Address
    from trezor.messages.FailureType import ProcessError
    from ..common import coins
    from ..common import seed
    from ..wallet.sign_tx import addresses

    if msg.multisig:
        raise wire.FailureError(ProcessError, 'GetAddress.multisig is unsupported')

    address_n = msg.address_n or ()
    coin_name = msg.coin_name or 'Bitcoin'
    coin = coins.by_name(coin_name)

    node = await seed.derive_node(ctx, address_n)

    address = addresses.get_address(msg.script_type, coin, node)
    res = False
    if msg.show_display:
        while not res:
            res = await _show_address(ctx, address)
            if not res:
                res = await _show_qr(ctx, address)

    return Address(address=address)

async def _show_qr(ctx, address):
    from trezor.messages.ButtonRequestType import Address
    from trezor.ui.text import Text
    from trezor.ui.qr import Qr
    from trezor.ui.container import Container
    from ..common.confirm import confirm

    content = Container(
        Qr(address, (120, 115), 4),
        Text('Confirm address', ui.ICON_RESET, ui.MONO))
    return await confirm(ctx, content, code=Address, cancel='Address', cancel_style=ui.BTN_KEY)

async def _show_address(ctx, address):
    from trezor.messages.ButtonRequestType import Address
    from trezor.ui.text import Text
    from trezor.ui.container import Container
    from ..common.confirm import confirm

    lines = _split_address(address)
    content = Container(Text('Confirm address', ui.ICON_RESET, ui.MONO, *lines))
    return await confirm(ctx, content, code=Address, cancel='QR', cancel_style=ui.BTN_KEY)


def _split_address(address):
    from trezor.utils import chunks
    return chunks(address, 17)
