import { ContactComponent }   from "./contact.component";
import { ContactService }     from "./contact.service";
import { Contact }            from "./contact";

describe("ContactComponent", () => {

    beforeEach(function() {
        this.cc = new ContactComponent(new ContactService(), null);
    });

    it("check if error message is set", function () {
        this.cc.displayError({"status": 500, "error": {"errors": "wrong"}});
        expect(this.cc.contactErrorMessage).toEqual("Fehler bei der Kontaktaufnahme: \nInterner Fehler, wrong");
    });

    it("check if error message is set (status 400)", function () {
        this.cc.displayError({"status": 400, "error": {"errors": {"name": "exceeds 50", "email": "wrong"}}});
        expect(this.cc.contactErrorMessage).toEqual("Fehler bei der Kontaktaufnahme: \n" +
            "name: exceeds 50 \nemail: wrong \n");
    });

    it("check if error message is cleared", function () {
        this.cc.displayError({"status": 500, "error": {"errors": "wrong"}});
        this.cc.clearError();
        expect(this.cc.contactErrorMessage).toEqual("");
    });

    it("check on file change too long file name", function () {
        this.cc.onFileChange({"srcElement": {"files": [{"name":
            "12345678901234567890123456789012345678901234567890.txt"}]}});
        expect(this.cc.filesValid).toEqual(false);
        expect(this.cc.contactErrorMessage).toEqual("Name des Anhangs '" +
                   "12345678901234567890123456789012345678901234567890.txt' zu lang (maximal 50 Zeichen)\n");
    });

    it("check on file change correct filename", function () {
        this.cc.onFileChange({"srcElement": {"files": [{"name": "1234567890.txt"}]}});
        expect(this.cc.filesValid).toEqual(true);
        expect(this.cc.uploads).toEqual([{"name": "1234567890.txt"}]);
    });

    it("check initilization", function() {
        expect(this.cc.contact).toEqual(new Contact("", "", "", "", null, null));
        expect(this.cc.filesValid).toEqual(true);
    });

    it("check on success display correct message", function() {
        this.cc.displaySuccess();
        expect(this.cc.contactSuccessMessage).toEqual("Vielen Dank! " +
            "Wir werden Ihre Anfrage schnellstmöglich bearbeiten!");
    });

    it("check on success reset of message", function() {
        this.cc.displaySuccess();
        let tmpCC = this;
        setTimeout(function(){
            expect(tmpCC.cc.contactSuccessMessage).toEqual("");
        }, 5000);
    });
});
