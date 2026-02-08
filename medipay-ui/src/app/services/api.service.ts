import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable } from 'rxjs';

@Injectable({
  providedIn: 'root'
})
export class ApiService {
  private javaUrl = 'http://localhost:8080/api/claims';
  private pythonUrl = 'http://localhost:5001/analytics/summary';

  constructor(private http: HttpClient) { }

  // Get data from Java
  getClaims(): Observable<any[]> {
    return this.http.get<any[]>(this.javaUrl);
  }

  // Update data in Java
  updateClaimStatus(id: number, status: string): Observable<any> {
    return this.http.put(`${this.javaUrl}/${id}/status?status=${status}`, {});
  }

  // Capture new claim in Java
  submitClaim(claim: any): Observable<any> {
  return this.http.post('http://localhost:8080/api/claims', claim);
  }
  // Get data from Python
  getStats(): Observable<any> {
    return this.http.get<any>(this.pythonUrl);
  }
}