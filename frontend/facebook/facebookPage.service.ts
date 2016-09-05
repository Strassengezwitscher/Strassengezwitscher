import { Injectable } from "@angular/core";
import { Http, Response } from "@angular/http";

import { FacebookPage } from "./facebookPage";
import { Observable } from "rxjs/Observable";

@Injectable()
export class FacebookPageService {
    private facebookPageUrl = "api/facebook/";

    constructor(private http: Http) {}

    public getFacebookPage(id: number): Observable<FacebookPage> {
        return this.http.get(this.facebookPageUrl + id + "/")
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
