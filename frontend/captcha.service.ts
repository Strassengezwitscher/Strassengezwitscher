import { Injectable }     from "@angular/core";
import { Http, Response, Headers, RequestOptions } from "@angular/http";
import { Observable }     from "rxjs/Observable";

@Injectable()
export class CaptchaService {

    private captchaUrl = "api/captcha/";

    constructor(private http: Http) {}

    public validateCaptcha (response: any): Observable<Response> {
    let body = JSON.stringify({ response });
    let headers = new Headers({ "Content-Type": "application/json" });
    let options = new RequestOptions({ headers: headers });
    return this.http.post(this.captchaUrl, body, options)
                    .map(this.handleResponse)
                    .catch(this.handleError);
    }

    private handleResponse(response: Response) {
        return response.json();
    }

    private handleError(error: any) {
        let errorMessage = "Interner Fehler im Captcha: \n";
        let errors = JSON.parse(error._body).errors;
        if (errors.length) {
            for (let msg of errors) {
                errorMessage += msg + " \n";
            }
        } else if (error.status) {
            errorMessage = `${error.status} - ${error.statusText}`;
        }
        return Observable.throw(errorMessage);
    }
}
