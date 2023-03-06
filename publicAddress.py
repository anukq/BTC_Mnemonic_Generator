import binascii
import hashlib
import hmac


def generate_receive_address_from_mnemonic(mnemonic):
    # Generate the seed from the mnemonic
    seed = hashlib.pbkdf2_hmac('sha512', mnemonic.encode('utf-8'), b'mnemonic', 2048)
    master_private_key = seed[:32]
    master_chain_code = seed[32:]

    # Derive the child private key from the master private key and chain code
    index = 0  # Use index 0 for the first receive address
    extended_private_key = b'\x04\x88\xad\xe4' + b'\x00' * 9 + master_private_key + master_chain_code
    for i in range(4):
        if index & 0x80000000:
            extended_private_key += hmac.digest(master_chain_code,
                                                b'\x00' + master_private_key + index.to_bytes(4, 'big'),
                                                hashlib.sha512)[:32]
        else:
            extended_private_key += hmac.digest(master_chain_code,
                                                extended_private_key[-32:] + index.to_bytes(4, 'big'), hashlib.sha512)[
                                    :32]
        index += 1  # Increment index inside the loop

    # Derive the child public key from the child private key
    extended_public_key = b'\x04\x88\xb2\x1e' + b'\x00' * 9 + hmac.digest(master_chain_code, extended_private_key[4:],
                                                                          hashlib.sha512)[:32] + extended_private_key[
                                                                                                 -32:]
    index = 0  # Reset index for child public key derivation
    for i in range(4):
        extended_public_key += hmac.digest(master_chain_code, extended_public_key[-32:] + index.to_bytes(4, 'big'),
                                           hashlib.sha512)[:32]
        index += 1  # Increment index inside the loop

    # Generate the receive address from the child public key
    public_key = extended_public_key[-33:]
    ripemd160 = hashlib.new('ripemd160')
    ripemd160.update(hashlib.sha256(public_key).digest())
    receive_address = '00' + binascii.hexlify(ripemd160.digest()).decode()

    # Compute the checksum of the receive address
    checksum = hashlib.sha256(hashlib.sha256(binascii.unhexlify(receive_address)).digest()).digest()[:4]
    checksum_hex = binascii.hexlify(checksum).decode()

    # Add the checksum to the receive address
    receive_address += checksum_hex

    # Convert the receive address to base58 encoding
    alphabet = '123456789ABCDEFGHJKLMNPQRSTUVWXYZabcdefghijkmnopqrstuvwxyz'
    receive_address_bytes = binascii.unhexlify(receive_address)
    receive_address_base58 = ''
    n = int.from_bytes(receive_address_bytes, byteorder='big')
    while n > 0:
        n, r = divmod(n, 58)
        receive_address_base58 = alphabet[r] + receive_address_base58

    # Add leading '1's for each leading zero byte
    i = 0
    while i < len(receive_address_bytes) and receive_address_bytes[i] == 0:
        receive_address_base58 = '1' + receive_address_base58
        i += 1

    return receive_address_base58
