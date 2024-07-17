export interface Breach {
  id: number;
  name: string;
  description: string;
  // breach_date: Date;
  breach_date: string;
  created_at: string;
  breached_data: string[];
  security_tips: string[];
  is_sensitive: boolean;
}

export interface DataLeak {
  data_type: string;
  breach: Breach;
  found_with: string[];
}
