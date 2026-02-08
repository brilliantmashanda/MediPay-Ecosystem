import { Component, OnInit } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms'; 
import { ApiService } from './services/api.service';
import { interval } from 'rxjs';

@Component({
  selector: 'app-root',
  standalone: true,
  imports: [CommonModule, FormsModule], 
  templateUrl: './app.component.html',
  styleUrls: ['./app.component.css']
})
export class AppComponent implements OnInit {
  claims: any[] = [];
  stats: any = null;

  newClaim = {
    patientName: '',
    patientSurname: '',
    claimAmount: 0,
    status: 'PENDING' ,
    providerName: '', 
    providerNo: ''
  };

  constructor(private api: ApiService) {}

  ngOnInit() {
    this.refreshData();
    interval(30000).subscribe(() => {
    this.refreshData();
  });
  }

  refreshData() {
    this.api.getClaims().subscribe(data => this.claims = data);
    this.api.getStats().subscribe(data => this.stats = data);
  }

  saveClaim() {
    if (this.newClaim.patientName && this.newClaim.claimAmount > 0) {
      this.api.submitClaim(this.newClaim).subscribe({
        next: () => {
          this.refreshData(); 
          this.resetForm();
        },
        error: (err) => console.error("Error saving claim:", err)
      });
    }
  }
  resetForm() {
    this.newClaim = {
      patientName: '',
      patientSurname: '',
      claimAmount: 0,
      status: 'PENDING',
      providerName: '',
      providerNo: ''
    };
  }

  approveClaim(id: number) {
    this.api.updateClaimStatus(id, 'APPROVED').subscribe(() => this.refreshData());
  }
}