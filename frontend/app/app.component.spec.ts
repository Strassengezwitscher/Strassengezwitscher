import { AppComponent } from "./app.component";

describe("AppComponent", () => {

  beforeEach(function() {
    this.app = new AppComponent();
  });

  it("true is true", () => expect(true).toEqual(true));

});
