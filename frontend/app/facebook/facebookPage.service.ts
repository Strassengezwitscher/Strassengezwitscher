import { Injectable } from "@angular/core";
import { Http, Response, Headers, RequestOptions } from "@angular/http";

import { FacebookPage } from "./facebookPage.model";
import { Observable } from "rxjs/Observable";

@Injectable()
export class FacebookPageService {
    private facebookPageUrl = "api/facebook/";
    private facebookPageCreateUrl = "api/facebook/new/";

    constructor(private http: Http) {}

    public getFacebookPage(id: number): Observable<FacebookPage> {
        let headers = new Headers({ "Accept": "application/json" });
        let options = new RequestOptions({ headers: headers });
        return this.http.get(this.facebookPageUrl + id + "/", options)
                        .map(this.extractData)
                        .catch(this.handleError);
    }

    public addFacebookPage (fbPage: FacebookPage) {
        let headers = new Headers({ "Content-Type": "application/json" });
        let options = new RequestOptions({ headers: headers });

        return this.http.post(this.facebookPageCreateUrl, fbPage, options)
                        .map(this.extractData)
                        .catch(this.handleError);

    }

    private extractData(response: Response): FacebookPage {
        let data = response.json();
        return <FacebookPage> data;
    }

    private handleError(error: any) {
        let errorMessage = "Server error";
        if (error.message) {
            errorMessage = error.message;
        } else if (error.status) {
            errorMessage = `${error.status} - ${error.statusText}`;
        }
        console.error(errorMessage);
        return Observable.throw(errorMessage);
    }
}
