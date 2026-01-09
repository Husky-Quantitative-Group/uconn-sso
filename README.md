A flask server that implements UConn SSO and returns recieved information about the user.

---

Example response from UConn CAS server:
```xml
<cas:serviceResponse xmlns:cas='http://www.yale.edu/tp/cas'>
    <cas:authenticationSuccess>
        <cas:user>abc12345</cas:user>
        
    </cas:authenticationSuccess>
</cas:serviceResponse>
```