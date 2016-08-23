import { ContactSuccessComponent } from "./contactSuccess.component";

describe("ContactComponent", () => {

    beforeEach(function() {
        this.csc = new ContactSuccessComponent();
    });

    it("Should set the contactSuccessMessage", function () {
        expect(this.csc.contactSuccessMessage).toEqual("Vielen Dank! " +
                                                       "Wir werden Ihre Anfrage schnellstmöglich bearbeiten!");
    });
});
