import { Injectable } from '@angular/core';
import { Constants } from './constants';
import { HttpClient } from '@angular/common/http';
import { Excel } from './model/excel'

@Injectable({
  providedIn: 'root'
})
export class ExcelService {

  constructor(
    private constants: Constants,
    private http: HttpClient
  ) {
  }

  sendProgramValidation(excelFile: FormData) {
    return this.http.post(this.constants.BASE_URL + this.constants.BASE_HREF + '/program', excelFile, {responseType: "blob"});
  }

  sendResourceValidation(excelFile: FormData) {
    return this.http.post(this.constants.BASE_URL + this.constants.BASE_HREF + '/resource', excelFile, {responseType: "blob"});
  }

  getColorPalette(document?: string) {
    let urlParams = document ? {doc: document} : {};
    return this.http.get(this.constants.BASE_URL + '/excel', {
      params: urlParams
    });
  }

  addColorPalette(color: String, document?: string) {
    let urlParams = document ? {doc: document} : {};
    return this.http.post(this.constants.BASE_URL + '/excel/add', color, {
      params: urlParams
    });
  }

}
