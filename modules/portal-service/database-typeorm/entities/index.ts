import {
  Entity,
  PrimaryGeneratedColumn,
  PrimaryColumn,
  ManyToOne,
  JoinColumn,
  Column,
  CreateDateColumn,
} from 'typeorm';

@Entity('users')
export class DMUser {
  @PrimaryColumn('uuid')
  id: string;
}

@Entity('tasks')
export class DMTask {
  @PrimaryGeneratedColumn('uuid')
  id: string;

  @ManyToOne(() => DMUser, {
    onDelete: 'SET NULL',
    onUpdate: 'CASCADE',
  })
  @JoinColumn({
    name: 'user_id',
  })
  user: DMUser;

  @Column({
    nullable: false,
    type: 'uuid',
  })
  user_id: string;

  @Column({
    type: 'varchar',
    length: 16,
    nullable: false,
  })
  command: string;

  @Column({
    type: 'text',
    nullable: true,
  })
  result: string;

  @Column({
    type: 'text',
    nullable: true,
  })
  input: string;

  @Column({
    type: 'varchar',
    length: 16,
    nullable: false,
  })
  status: string;

  @Column({
    type: 'text',
    nullable: true,
  })
  reason: string;

  @CreateDateColumn()
  created_at: Date;
}
