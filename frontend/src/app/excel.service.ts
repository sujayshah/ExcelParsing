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

  sendProgramValidation(excelFile: Excel) {
    return this.http.post<File>(this.constants.BASE_URL + this.constants.BASE_HREF + '/program', excelFile);
  }

  sendResourceValidation(excelFile: Excel) {
    return this.http.post<File>(this.constants.BASE_URL + this.constants.BASE_HREF + '/resource', excelFile);
  }
}
