from lifeos import vault

def test_vault_import():
    # Vault should load without error
    assert vault is not None
