import { Observable } from "rxjs/Rx";
import { TestBed, inject } from "@angular/core/testing";

import { FacebookPage } from "./facebookPage.model";
import { FacebookPageComponent } from "./facebookPage.component";
import { FacebookPageService } from "./facebookPage.service";

class MockFacebookPageService {
    public getFacebookPage(id: number): Observable<FacebookPage> {
        let fb = new FacebookPage();
        fb.id = 1;
        fb.name = "Test";
        if (id === 1) {
            return new Observable<FacebookPage>(observer => {
                observer.next(fb);
                observer.complete();
            });
        } else {
            return Observable.throw(new Error("error"));
        }
    }
}

describe("FacebookPageComponent", () => {

    beforeEach(() => {
        TestBed.configureTestingModule({
            providers: [
                FacebookPageComponent,
                {
                    provide: FacebookPageService,
                    useClass: MockFacebookPageService,
                },
            ],
        });
    });

    it("Should set the active Page", inject([FacebookPageComponent], (fbPageComponent)  => {
        let fbPage = new FacebookPage();
        fbPageComponent.setActivePage(fbPage);
        expect(fbPageComponent.activePage).toBe(fbPage);
    }));

    it("Should set a new active Page", inject([FacebookPageComponent], (fbPageComponent) =>  {
        fbPageComponent.getFacebookPageDetails(1);
        expect(fbPageComponent.activePage.id).toBe(1);
    }));

    it("Should set a new active Page on ngChange", inject([FacebookPageComponent], (fbPageComponent) =>  {
        fbPageComponent.id = 1;
        fbPageComponent.ngOnChanges({"id": 125});
        expect(fbPageComponent.activePage.name).toBe("Test");
    }));

    it("Should throw emit an error", inject([FacebookPageComponent], (fbPageComponent) =>  {
        spyOn(fbPageComponent.onError, "emit");
        fbPageComponent.getFacebookPageDetails(10);
        expect(fbPageComponent.onError.emit).toHaveBeenCalledTimes(1);
    }));

});
