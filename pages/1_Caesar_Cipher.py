import streamlit as st

def encrypt_decrypt(text, shift_keys, ifdecrypt):
    result = ""
    shiftKeyLen = len(shift_keys)
    for start, char in enumerate(text):
        shift_key = shift_keys[start % shiftKeyLen] if not ifdecrypt else -shift_keys[start % shiftKeyLen]
        
        result += chr((ord(char) + shift_key - 32) % 94 + 32)
        st.write(start, char, shift_keys[start % shiftKeyLen], result[start])
        
    return result
    

if __name__ == "__main__":
    # Example usage
    text = st.text_area("", key=143)
    shift_keys = list(map(int, st.text_area("").split()))

    if st.button("Encrypt"):
        encreypted = encrypt_decrypt(text, shift_keys, False)
        st.write("----------")
        Decrypted = encrypt_decrypt(encreypted, shift_keys, True)
        st.write("----------")
        
        st.write("Text:", text)
        st.write("Shift keys:" , " ".join(map(str, shift_keys)))
        st.write("Cipher:",  encreypted)
        st.write("Decrypted text:", Decrypted)
    
